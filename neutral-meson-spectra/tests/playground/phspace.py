#!/usr/bin/python


import ROOT

import json
import tqdm

from array import array
from itertools import combinations, product

from spectrum.sutils import tsallis
from spectrum.outputcreator import output_histogram


def particle(pt, mass=0):
    # x, y, z = ROOT.Double(0), ROOT.Double(0), ROOT.Double(0)
    # pt / cos theta = p
    # p = pt / random()
    # ROOT.gRandom.Sphere(x, y, z, p)
    # return ROOT.TLorentzVector(x, y, z, (p ** 2 + mass ** 2) ** 0.5)
    return ROOT.TLorentzVector(pt, 0, 0, (pt ** 2 + mass ** 2) ** 0.5)


class BackgroundGenerator(object):
    def __init__(self, raw_gamma_pectrum, meanphotons=10.):
        super(BackgroundGenerator, self).__init__()
        self.spectrum = raw_gamma_pectrum
        self.meanphotons = meanphotons

    def generate(self):
        if self.meanphotons == 0:
            return []

        nphotons = int(ROOT.gRandom.Exp(1. / self.meanphotons))
        return [particle(self.spectrum.GetRandom()) for i in range(nphotons)]


class SignalGenerator(object):
    def __init__(self, config, genhistname, generated=None):
        super(SignalGenerator, self).__init__()
        ptbins = self._configure(config)
        self.generated = generated if generated else (
            output_histogram(genhistname, "Generated spectrum",
                             "").get_hist(ptbins, [])
        )

    def _configure(self, conffile):
        with open(conffile) as f:
            conf = json.load(f)

        self.true_mass = ROOT.TF1(*conf['fmass'])
        self.true_mass.SetParameters(*conf['true_mass'])

        self.true_width = ROOT.TF1(*conf['fwidth'])
        self.true_width.SetParameters(*conf['true_width'])

        emin, emax = conf['erange']
        self.true_spectrum = ROOT.TF1(
            'fTsallis', lambda x, p: tsallis(x, p), emin, emax, 3)
        self.true_spectrum.SetParameters(*conf['true_spectrum'])
        self.average_nmesons = conf['average_nmesons']
        return conf['pt_edges']

    def generate(self):
        nmesons = 1  # int(ROOT.gRandom.Exp(1. / self.average_nmesons))
        mesons = [self._generate_meson() for i in range(nmesons)]
        return sum(mesons, [])

    def _generate_meson(self):
        pt = self.random_momentum()
        mass = self._random_mass(pt)

        pi0 = particle(pt, mass)
        self.generated.Fill(pi0.Pt())

        event = ROOT.TGenPhaseSpace()
        nphot, masses = 2, array('d', [0, 0])
        event.SetDecay(pi0, nphot, masses)
        event.Generate()

        return [event.GetDecay(i) for i in range(nphot)]

    def _random_mass(self, pt):
        mass, width = self.true_mass.Eval(pt), self.true_width.Eval(pt)
        gen_mass = ROOT.gRandom.Gaus(mass, width)
        return gen_mass

    def random_momentum(self):
        pt = self.true_spectrum.GetRandom(ROOT.Double(0.8), ROOT.Double(20))
        return pt


class FlatGenerator(SignalGenerator):
    def __init__(self, config, genhistname, generated=None):
        super(FlatGenerator, self).__init__(config, genhistname, generated)

    def _random_mass(self, pt):
        gen_mass = ROOT.gRandom.Gaus(0.135, 0.005)
        return gen_mass

    def random_momentum(self):
        pt = ROOT.gRandom.Uniform(ROOT.Double(0.8), ROOT.Double(20))
        return pt


class InclusiveGenerator(object):
    def __init__(self,
                 fname,
                 signalconf,
                 selname='PhysOnlyTender',
                 hnames=['hMassPt', 'hMixMassPt', 'EventCounter'],
                 hpdistr='hClusterPt_SM0',
                 genfilename='LHC16-fake.root',
                 genhistname='hPt_#pi^{0}_primary',
                 meanphotons=0,
                 flat=False
                 ):
        super(InclusiveGenerator, self).__init__()
        self.selname = selname
        self.genfilename = genfilename
        self.backgrnd = BackgroundGenerator(
            self.read(fname, hpdistr), meanphotons=meanphotons)
        self.data, self.mixed, self.nevents = map(
            lambda y: self.read(fname, y, True), hnames)
        generated = self.read(fname, genhistname + '_',
                              True) if genhistname else None

        GenType = SignalGenerator if not flat else FlatGenerator
        self.signal = GenType(signalconf, genhistname, generated)
        self.out = [self.data, self.mixed, self.nevents, self.signal.generated]
        self.update_hists()

    def read(self, fname, name, reset=False):
        print fname, name, reset
        lst = ROOT.TFile(fname).Get(self.selname)
        obj = lst.FindObject(name)
        if reset:
            obj.Reset()
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
        for i in tqdm.trange(nevents):
            photons = self.fill(self.signal.generate() +
                                self.backgrnd.generate(), mixed)
            mixed.append(photons)

            if len(mixed) > 100:
                mixed.pop()

        # Just fill event counter
        self.nevents.Fill(1, nevents)
        self.save_fake()
        return self.signal.generated

    def fill(self, photons, mixed):
        def masspt(x):
            return (x.M(), x.Pt())

        for combination in combinations(photons, 2):
            self.data.Fill(*masspt(sum(combination, ROOT.TLorentzVector())))

        for previous in mixed:
            for combination in product(photons, previous):
                self.mixed.Fill(
                    *masspt(sum(combination, ROOT.TLorentzVector())))

        # just return untouched to update mixed events
        return photons
