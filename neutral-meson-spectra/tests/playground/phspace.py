from __future__ import print_function
import ROOT

import json
import tqdm

from array import array
from itertools import combinations, product

from spectrum.outputcreator import output_histogram
from vault.formulas import FVault


def tsallis(rrange=(0., 20.)):
    tsallis = ROOT.TF1("f", FVault().func("tsallis"), *rrange)
    tsallis.SetParameters(0.0149, 0.2878, 9.9210)
    tsallis.FixParameter(3, 0.135)
    tsallis.FixParameter(4, 0.135)
    tsallis.SetLineColor(ROOT.kRed + 1)
    return tsallis


def particle(pt, mass=0):
    x, y, z = ROOT.Double(0), ROOT.Double(0), ROOT.Double(0)
    # pt / cos theta = p
    ROOT.gRandom.Sphere(x, y, z, pt)
    return ROOT.TLorentzVector(x, y, z, (pt ** 2 + mass ** 2) ** 0.5)


class BackgroundGenerator(object):
    def __init__(self, raw_gamma_pectrum, mean_photons=10.):
        super(BackgroundGenerator, self).__init__()
        self.spectrum = raw_gamma_pectrum
        self.mean_photons = mean_photons

    def generate(self):
        if self.mean_photons == 0:
            return []

        nphotons = int(ROOT.gRandom.Exp(1. / self.mean_photons))
        return [particle(self.spectrum.GetRandom()) for i in range(nphotons)]


class SignalGenerator(object):
    def __init__(self, config, gen_hist_name, generated=None):
        super(SignalGenerator, self).__init__()
        ptbins = self._configure(config)
        self.generated = generated if generated else (
            output_histogram(gen_hist_name, "Generated spectrum",
                             "").get_hist(ptbins, [])
        )

    def _configure(self, conffile):
        with open(conffile) as f:
            conf = json.load(f)

        self.true_mass = ROOT.TF1(*conf['fmass'])
        self.true_mass.SetParameters(*conf['true_mass'])

        self.true_width = ROOT.TF1(*conf['fwidth'])
        self.true_width.SetParameters(*conf['true_width'])

        self.true_spectrum = tsallis(conf['erange'])
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
    def __init__(self, config, gen_hist_name, generated=None):
        super(FlatGenerator, self).__init__(config, gen_hist_name, generated)

    def _random_mass(self, pt):
        gen_mass = ROOT.gRandom.Gaus(0.135, 0.005)
        return gen_mass

    def random_momentum(self):
        pt = ROOT.gRandom.Uniform(ROOT.Double(0.8), ROOT.Double(20))
        return pt


class InclusiveGenerator(object):
    def __init__(self,
                 fname,
                 signal_conf,
                 selname='PhysOnlyTender',
                 hnames=['hMassPt', 'hMixMassPt', 'EventCounter'],
                 hpdistr='hClusterPt_SM0',
                 gen_file_name='LHC16-fake.root',
                 gen_hist_name='hPt_#pi^{0}_primary',
                 mean_photons=0,
                 flat=False
                 ):
        super(InclusiveGenerator, self).__init__()
        self.selname = selname
        self.gen_file_name = gen_file_name
        self.backgrnd = BackgroundGenerator(
            self.read(fname, hpdistr), mean_photons=mean_photons)
        self.data, self.mixed, self.nevents = map(
            lambda y: self.read(fname, y, True), hnames)
        generated = self.read(fname, gen_hist_name + '_',
                              True) if gen_hist_name else None

        GenType = SignalGenerator if not flat else FlatGenerator
        self.signal = GenType(signal_conf, gen_hist_name, generated)
        self.out = [self.data, self.mixed, self.nevents, self.signal.generated]
        self.update_hists()

    def read(self, fname, name, reset=False):
        print(fname, name, reset)
        lst = ROOT.TFile(fname).Get(self.selname)
        obj = lst.FindObject(name)
        if reset:
            obj.Reset()
        return obj

    def update_hists(self):
        ofile = ROOT.TFile(self.gen_file_name)
        olist = ofile.Get(self.selname)

        if not olist:
            return

        print('WARNING: You are trying to update the old histograms.')

        def process(hist):
            ohist = olist.FindObject(hist.GetName())
            hist.Add(ohist)

        map(process, self.out)
        ofile.Close()

    def save_fake(self):
        ofile = ROOT.TFile(self.gen_file_name, 'recreate')
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
