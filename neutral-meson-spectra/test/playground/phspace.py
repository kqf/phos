#!/usr/bin/python


import ROOT
import progressbar
import json
from itertools import combinations, product
from spectrum.sutils import tsallis
from spectrum.ptanalyzer import PtDependent
from array import array
from random import random

def particle(pt, mass = 0):
    x, y, z = ROOT.Double(0), ROOT.Double(0), ROOT.Double(0)
    # pt / cos theta = p
    # p = pt / random()
    # ROOT.gRandom.Sphere(x, y, z, p)
    # return ROOT.TLorentzVector(x, y, z, (p ** 2 + mass ** 2) ** 0.5)
    return ROOT.TLorentzVector(pt, 0, 0, (pt ** 2 + mass ** 2) ** 0.5)


class BackgroundGenerator(object):
    def __init__(self, raw_gamma_pectrum, meanphotons = 10.):
        super(BackgroundGenerator, self).__init__()
        self.spectrum = raw_gamma_pectrum
        self.meanphotons = meanphotons

    def generate(self):
        if self.meanphotons == 0:
            return []
            
        nphotons = int(ROOT.gRandom.Exp(1. / self.meanphotons))
        return [particle(self.spectrum.GetRandom()) for i in range(nphotons)]



# TODO: Swap definitions of the classes SignalGenerator, FlatGenerator
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
        nmesons = 4 #int(ROOT.gRandom.Exp(1. / self.average_nmesons))
        mesons = [self.generate_meson() for i in range(nmesons)]
        return sum(mesons, [])


    def generate_meson(self):
        pt = self.random_momentum()
        mass = self.random_mass(pt)

        pi0 = particle(pt, mass)
        self.generated.Fill(pi0.Pt())

        event = ROOT.TGenPhaseSpace()
        nphot, masses = 2, array('d', [0, 0])
        event.SetDecay(pi0, nphot, masses)
        event.Generate()

        return [event.GetDecay(i) for i in range(nphot)]


    def random_mass(self, pt):
        mass, width = self.true_mass.Eval(pt), self.true_width.Eval(pt)
        gen_mass = ROOT.gRandom.Gaus(mass, width)
        return gen_mass

    def random_momentum(self):
        pt = self.true_spectrum.GetRandom(ROOT.Double(0.8), ROOT.Double(20))
        return pt



class FlatGenerator(SignalGenerator):
    def __init__(self, config):
        super(FlatGenerator, self).__init__(config)


    def random_mass(self, pt):
        gen_mass = ROOT.gRandom.Gaus(0.135, 0.005)
        return gen_mass

    def random_momentum(self):
        pt = ROOT.gRandom.Uniform(ROOT.Double(0.8), ROOT.Double(20))
        return pt



class InclusiveGenerator(object):
    def __init__(self, fname, signalconf, selname = 'PhysNonlinTender', 
                 hnames = ['hMassPtN3', 'hMixMassPtN3', 'EventCounter'], hpdistr='hClusterPt_SM0', genfilename = 'LHC16-fake.root', meanphotons = 0, flat = False):
        super(InclusiveGenerator, self).__init__()
        self.selname = selname
        self.genfilename = genfilename
        self.signal = SignalGenerator(signalconf) if not flat else FlatGenerator(signalconf)
        self.backgrnd = BackgroundGenerator(self.read(fname, hpdistr), meanphotons = meanphotons)
        self.data, self.mixed, self.nevents = map(lambda y: self.read(fname, y, True), hnames)
        self.out = [self.data, self.mixed, self.nevents, self.signal.generated]
        self.update_hists()


    def read(self, fname, name, reset = False):
        lst = ROOT.TFile(fname).Get(self.selname)
        obj = lst.FindObject(name)
        if reset: obj.Reset()
        return obj


    def update_hists(self):
        ofile = ROOT.TFile(self.genfilename)
        olist = ofile.Get(self.selname)

        if not olist:
            return

        print 'WARNING: You are trying to update the old histograms.'
        def process(hist):
            ohist = olist.FindObject(hist.GetName()) 
            hist.Add(ohist)

        map(process, self.out)
        ofile.Close()


    def save_fake(self):
        ofile = ROOT.TFile(self.genfilename, 'recreate')
        olist = ROOT.TList()
        olist.SetName(self.selname)
        map(olist.Add, self.out)
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
        self.save_fake()
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
