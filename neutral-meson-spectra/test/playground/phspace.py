#!/usr/bin/python


import ROOT
from itertools import combinations, product


class BackgroundGenerator(object):
    def __init__(self, raw_gamma_pectrum):
        super(BackgroundGenerator, self).__init__()
        self.spectrum = raw_gamma_pectrum

    def generate(self):
        # TODO: add multiple pi0s
        # TODO: add spherical distribution
        p = self.spectrum.GetRandom()
        return [ROOT.TLorentzVector(0, 0, p, p)]

    def generated_signal(self):
        # TODO: return here something meaningfull
        pass


class SignalGenerator(object):
    def __init__(self, config):
        super(SignalGenerator, self).__init__()
        self.config = config

    def generate(self):
        # TODO: add phase space dependence
        # TODO: add mass/sigma pt dependence
        return [ROOT.TLorentzVector(0, 0, 0, 0), ROOT.TLorentzVector(0, 0, 0, 0.135)]


class InclusiveGenerator(object):
    def __init__(self, fname, selname = 'PhysTender', 
                 hnames = ['hMassPtN3', 'hMixMassPtN3', 'EventCounter'], hpdistr='hClusterPt_SM0'):
        super(InclusiveGenerator, self).__init__()
        self.selname = selname
        # TODO: we have to have Nevents here 
        # as we wil luse it later for reading and retreiving the data
        self.signal = SignalGenerator(None)
        self.backgrnd = BackgroundGenerator(self.read(fname, [hpdistr])[0])
        self.data, self.mixed, self.nevents = self.read(fname, hnames)


    def read(self, fname, hnames):
        lst = ROOT.TFile(fname).Get(self.selname)
        hist = lambda n: lst.FindObject(n)
        return map(hist, hnames)


    def save_fake(self, fname):
        ofile = ROOT.TFile(fname, 'recreate')
        olist = ROOT.TList()
        olist.Add(self.data)
        olist.Add(self.mixed)
        olist.Add(self.nevents)
        olist.Write(self.selname, 1)
        ofile.Close()


    def real_distributions(self, nevents):
        mixed = []
        for i in range(nevents):
            photons = self.fill(self.signal.generate() + self.backgrnd.generate(), mixed)
            mixed.append(photons)

            if len(mixed) > 100:
                mixed.pop()

        # Just fill event counter
        self.nevents.Fill(1, nevents)
        return self.signal.generated


    def fill(self, photons, mixed):
        masspt = lambda x: x.M(), x.Pt()

        for combination in combinations(photons):
            self.data.Fill(*masspt(sum(combination)))

        for previous in mixed:
            for combination in product(photons, previous):
                self.mixed.Fill(*masspt(sum(combination)))

        # just return untouched to update mixed events
        return photons  



