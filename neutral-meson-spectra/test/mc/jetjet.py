#!/usr/bin/python

from spectrum.spectrum import Spectrum
from spectrum.options import Options
from spectrum.input import Input, read_histogram
from spectrum.sutils import get_canvas, adjust_canvas
from spectrum.sutils import wait, scalew
from spectrum.comparator import Comparator
from spectrum.sutils import save_tobject

from test.analysis.test_check_different_modules import run_analysis

import ROOT

import os.path
import unittest


# This testcase is to check the Jet-Jet normalization
#


class Jetjet(unittest.TestCase):


    def setUp(self):
        self.selection = 'MCStudyOnlyTender'
        self.gen_histogram = 'hPt_#pi^{0}'
        self.rec_histogram = 'MassPt'

        # To compare more than 1 production
        self.productions = 'LHC17f8a', 'LHC17f8c'
        self.files = {'weighed': 'input-data/scaled-%s.root', 'no weights #times 10^{-3}': 'input-data/%s.root'}
        # self.files = {'ok': 'input-data/LHC17f8a.root'}


    def distribution(self, filename, histname, label, title):
        # Compare same selection

        hist = read_histogram(filename, self.selection, histname, label = label, priority = 0, norm = True)
        hist.SetTitle('{0} {1}'.format(hist.GetTitle(), title))
        scalew(hist, 1e-3 if 'no' in label else 1)
        # scalew(hist, 1. / hist.Integral())
        hist.logy = True
        return hist 


    def testFiles(self):
        """
            To check files it's enough to check un/weighed generated spectra
        """
        for prod in self.productions:
            efficiencies = [self.distribution(f % prod, self.gen_histogram, k, prod) for k, f in self.files.iteritems()]
            diff = Comparator(rrange=(-1, -1), oname = 'MC_PHOS_generated_{0}'.format(prod))
            diff.compare(efficiencies)


    def reconstructed(self, filename, histname, label, title):
        inp = Input(filename, self.selection, histname)
        reco = Spectrum(inp, label= label, mode = 'd').evaluate()[2]
        reco.SetTitle('{0} {1}'.format(reco.GetTitle(), title))
        scalew(reco, 1e-3 if 'no' in label else 1)
        return reco


    def testProduction(self):
        """
            This is to check pi0 peak.
        """
        for prod in self.productions:
            efficiencies = [self.reconstructed(f % prod, self.rec_histogram, k, prod) for k, f in self.files.iteritems()]
            diff = Comparator((1, 1), rrange = (-1, -1), oname = 'MC_PHOS_reconstructed_{0}'.format(prod))
            diff.compare(efficiencies)
