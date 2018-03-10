#!/usr/bin/python

import ROOT
from spectrum.spectrum import Spectrum
from spectrum.input import Input
from spectrum.options import Options
from spectrum.broot import BROOT as br
from spectrum.comparator import Comparator
import spectrum.comparator as cmpr
import spectrum.sutils as su
from vault.datavault import DataVault

import unittest
import operator

# This test is used to determine the best background function for 
# eta meson invariant mass distribution
#

class TestBackgroundShape(unittest.TestCase):

    def setUp(self):
        files = {
            DataVault().file("single #eta", "low"): (2.2, 10),
            DataVault().file("single #eta", "high"): (10, 20)
        }

        labels = ('0 < p_{T} < 10', '4 < p_{T} < 100')

        inputs = [
            Input(f, 'PhysEffOnlyTender', label=l) 
            for l, f in zip(labels, files)
        ]
        options = [Options.spmc(rr, 
            particle='eta'
        ) for (f, rr) in files.iteritems()]

        self.arguments = inputs, options


    @unittest.skip('')
    def test_fix_cb_parameters(self):
        inputs, options = zip(*self.arguments)[0]
        options.param.relaxed = True

        low_pt = Spectrum(inputs, options).evaluate()

        diff = Comparator()
        # diff.compare(histograms)

        # Significnt region is 4 < p_T < 10
        fiftf = ROOT.TF1('cballtest', '[0]', 4, 10)
        fiftf.SetParameter(0, 1.1)

        low_pt.cball_alpha.Fit(fiftf, 'R')
        diff.compare(low_pt.cball_alpha)

        low_pt.cball_n.Fit(fiftf, 'R')
        diff.compare(low_pt.cball_n)
        su.wait()

    def test_new_cb_parameters(self):
       # Try to relax CB parameters 
        for opt in self.arguments[1]:
            print opt
            # opt.param.relaxed = True  

        estimators = map(Spectrum, *self.arguments)
        histograms = map(lambda x: x.evaluate(), estimators)

        diff = Comparator()
        diff.compare(histograms)

