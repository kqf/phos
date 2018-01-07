#!/usr/bin/python

import ROOT
from spectrum.spectrum import Spectrum
from spectrum.ptanalyzer import PtAnalyzer
from spectrum.input import Input
from spectrum.options import Options
from spectrum.broot import BROOT as br
from spectrum.comparator import Comparator
import spectrum.comparator as cmpr
import spectrum.sutils as su

import unittest
import operator

# This test is used to determine the best background function for 
# eta meson invariant mass distribution
#

class TestBackgroundShape(unittest.TestCase):

    def setUp(self):
        ddir = '/single/nonlin1/'
        files = (
                    (ddir + 'LHC17j3c1', (0, 10)),
                    (ddir + 'LHC17j3c2', (4, 20))
        )

        inputs = [Input(f, 'PhysEffOnlyTender').read() for (f, _) in files]
        options = [Options.spmc(rr, 
            particle='eta',
            paramconf = 'config/cball-parameters-spmc-test.json'

        ) for (f, rr) in files]

        self.arguments = inputs, options

    @unittest.skip('')
    def test_background_shape(self):
        f = lambda x, y: PtAnalyzer(x, y).plotter
        ptranges = map(f, *self.arguments)



        for r in self.results:
            for im in r.masses:
                im.extract_data()

            intgr_ranges = [(0.1, 0.2)] * len(r.masses)

            r.opt.show_img = True
            r._draw_mass(intgr_ranges)
            r._draw_signal(intgr_ranges)


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
            opt.param.relaxed = True  

        estimators = map(Spectrum, *self.arguments)
        histograms = map(lambda x: x.evaluate(), estimators)

        diff = Comparator()
        diff.compare(histograms)

