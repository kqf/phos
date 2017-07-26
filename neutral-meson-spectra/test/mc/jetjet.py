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
        self.histogram = 'hPt_#pi^{0}'

        # To compare more than 1 production
        self.files = {'weighed': 'input-data/scaled-LHC17f8a.root', 'no weights': 'input-data/LHC17f8a.root'}
        # self.files = {'ok': 'input-data/LHC17f8a.root'}


    def distribution(self, filename, histname, label):
        # Compare same selection
        hist = read_histogram(filename, self.selection, histname, label = label, priority = 0, norm = True)
        scalew(hist, 1. / hist.Integral())
        hist.logy = True
        return hist 


    def testFiles(self):
        efficiencies = [self.distribution(f, self.histogram, k) for k, f in self.files.iteritems()]
        diff = Comparator()
        diff.compare(efficiencies)

