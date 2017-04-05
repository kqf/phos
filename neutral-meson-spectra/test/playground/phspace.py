#!/usr/bin/python


import ROOT
import progressbar
import json
from itertools import combinations, product
from spectrum.sutils import tsallis
from spectrum.ptanalyzer import PtDependent
from array import array

def particle(pt, mass = 0):
    x, y, z = ROOT.Double(0), ROOT.Double(0), ROOT.Double(0)
    ROOT.gRandom.Sphere(x, y, z, pt)
    return ROOT.TLorentzVector(x, y, z, (pt ** 2 + mass ** 2) ** 0.5)

class BackgroundGenerator(object):
    def __init__(self, raw_gamma_pectrum, meanphotons = 10.):
        super(BackgroundGenerator, self).__init__()
        self.spectrum = raw_gamma_pectrum
        self.meanphotons = meanphotons

    def generate(self):
        nphotons = int(ROOT.gRandom.Exp(1. / self.meanphotons))
        return [particle(self.spectrum.GetRandom()) for i in range(nphotons)]



class SignalGenerator(object):
    def __init__(self, config):
        super(SignalGenerator, self).__init__()
        ptbins = self.configure(config)
        self.generated = PtDependent("hGenerated", "Generated spectrum", "Generated").get_hist(ptbins, [])


    def configure(self, conffile):
        with open(conffile) as f: 
            conf = json.load(f)

        self.true_mass  = ROOT.TF1(*conf['fmass'])
        self.true_mass.SetParameters(*conf['true_mass'])

        self.true_width = ROOT.TF1(*conf['fwidth'])
        self.true_width.SetParameters(*conf['true_width'])

        emin, emax = conf['erange']
        self.true_spectrum = ROOT.TF1('fTsallis', lambda x, p: tsallis(x, p), emin, emax, 3)
        self.true_spectrum.SetParameters(*conf['true_spectrum'])
        self.average_nmesons = conf['average_nmesons']
        return conf['pt_edges']


    def generate(self):
        nmesons = int(ROOT.gRandom.Exp(1. / self.average_nmesons))
        mesons = [self.generate_meson() for i in range(nmesons)]
        return sum(mesons, [])


    def generate_meson(self):
        pt = self.true_spectrum.GetRandom(ROOT.Double(0.8), ROOT.Double(20))
        mass, width = self.true_mass.Eval(pt), self.true_width.Eval(pt)
        gen_mass = ROOT.gRandom.Gaus(mass, width)

        pi0 = particle(pt, gen_mass)
        self.generated.Fill(pi0.Pt())

        event = ROOT.TGenPhaseSpace()
        nphot, masses = 2, array('d', [0, 0])
        event.SetDecay(pi0, nphot, masses)
        event.Generate()

        return [event.GetDecay(i) for i in range(nphot)]


class InclusiveGenerator(object):
    def __init__(self, fname, signalconf, selname = 'PhysTender', 
                 hnames = ['hMassPtN3', 'hMixMassPtN3', 'EventCounter'], hpdistr='hClusterPt_SM0'):
        super(InclusiveGenerator, self).__init__()
        self.selname = selname
        self.signal = SignalGenerator(signalconf)
        self.backgrnd = BackgroundGenerator(self.read(fname, hpdistr))
        self.data, self.mixed, self.nevents = map(lambda y: self.read(fname, y, True), hnames)


    def read(self, fname, name, reset = False):
        lst = ROOT.TFile(fname).Get(self.selname)
        obj = lst.FindObject(name)
        if reset: obj.Reset()
        return obj


    def save_fake(self, fname):
        ofile = ROOT.TFile(fname, 'recreate')
        olist = ROOT.TList()
        olist.Add(self.data)
        olist.Add(self.mixed)
        olist.Add(self.nevents)
        olist.Write(self.selname, 1)
        ofile.Close()


    def generate(self, nevents):
        mixed = []
        bar = progressbar.ProgressBar()
        for i in bar(range(nevents)):
            photons = self.fill(self.signal.generate() + self.backgrnd.generate(), mixed)
            mixed.append(photons)

            if len(mixed) > 100:
                mixed.pop()

        # Just fill event counter
        self.nevents.Fill(1, nevents)
        PtDependent.divide_bin_width(self.signal.generated)
        return self.signal.generated


    def fill(self, photons, mixed):
        masspt = lambda x: (x.M(), x.Pt())

        for combination in combinations(photons, 2):
            self.data.Fill(*masspt(sum(combination, ROOT.TLorentzVector())))

        for previous in mixed:
            for combination in product(photons, previous):
                self.mixed.Fill(*masspt(sum(combination, ROOT.TLorentzVector())))

        # just return untouched to update mixed events
        return photons  
