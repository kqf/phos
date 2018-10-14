#!/usr/bin/python

from spectrum.spectrum import Spectrum
from spectrum.options import Options
from spectrum.input import Input, read_histogram
from spectrum.comparator import Comparator


from spectrum.broot import BROOT as br

import unittest


# This testcase is to check the Jet-Jet normalization
#


class Jetjet(unittest.TestCase):

    def setUp(self):
        self.selection = 'MCStudyOnlyTender'
        self.gen_histogram = 'hPt_#pi^{0}'
        self.rec_histogram = 'MassPt'

        # To compare more than 1 production
        self.productions = 'LHC17f8a', 'LHC17f8c', 'LHC17f8d', 'LHC17f8e', 'LHC17f8f', 'LHC17f8j', 'LHC17f8g', 'LHC17f8k'
        self.files = {'weighed': 'input-data/scaled-%s.root',
                      'no weights #times 10^{-3}': 'input-data/%s.root'}
        # self.files = {'ok': 'input-data/LHC17f8a.root'}

    def distribution(self, filename, histname, label, title):
        # Compare same selection

        hist = read_histogram(filename, self.selection,
                              histname, label=label, priority=0, norm=True)
        hist.SetTitle('{0} {1}'.format(hist.GetTitle(), title))
        const = 1e-3 if 'no' in label else 1
        br.scalew(hist, const * 1. / hist.Integral())
        hist.logy = 1
        return hist

    @unittest.skip('work on full production')
    def test_files(self):
        """
            To check files it's enough to check un/weighed generated spectra
        """
        for prod in self.productions:
            gen = [self.distribution(f % prod, self.gen_histogram, k, prod)
                   for k, f in self.files.iteritems()]
            diff = Comparator(
                rrange=(-1, -1), oname='MC_PHOS_generated_{0}'.format(prod))
            diff.compare(gen)

    def reconstructed(self, filename, histname, label, title):
        inp = Input(filename, self.selection, histname, label=label)
        reco = Spectrum(inp, Options(mode='d')).evaluate().spectrum
        reco.logy = 1
        reco.SetTitle('{0} {1}'.format(reco.GetTitle(), title))
        br.scalew(reco, 1e-3 if 'no' in label else 1)
        return reco

    @unittest.skip('work on full production')
    def test_different_productions(self):
        """
            This is to check pi0 peak.
        """
        for prod in self.productions:
            rec = [self.reconstructed(f % prod, self.rec_histogram, k, prod)
                   for k, f in self.files.iteritems()]
            diff = Comparator((1, 1), rrange=(-1, -1),
                              oname='MC_PHOS_reconstructed_{0}'.format(prod))
            diff.compare(rec)

    def test_full_production(self):
        inp = Input('pythia-jet-jet', 'PhysNonlinOnlyTender',
                    label='Pythia8 JJ')
        opt = Options('v', priority=1)
        opt.pt.rebins[-1] = 0
        results = Spectrum(inp, opt).evaluate().mass
        diff = Comparator()
        diff.compare(results)
