#!/usr/bin/python

from spectrum.ptanalyzer import PtAnalyzer
from spectrum.input import Input
from spectrum.options import Options
from spectrum.broot import BROOT as br
import spectrum.comparator as cmpr

import unittest
import operator

# This test is used to determine the best background function for 
# eta meson invariant mass distribution
#

class TestBackgroundShape(unittest.TestCase):

    def setUp(self):
        ddir = '/single/nonlin1/'
        files = {
                    ddir + 'LHC17j3c1': (0, 10),
                    ddir + 'LHC17j3c2': (4, 20)
                }

        inputs = [Input(f, 'PhysEffOnlyTender').read() for f in files]
        options = [Options.spmc(rr, particle='eta') for f, rr in files.iteritems()]
        for opt in options:
            opt.fitf = "gaus"

        f = lambda x, y: PtAnalyzer(x, y).plotter
        self.results = map(f, inputs, options)


    def test_background_shape(self):
        for r in self.results:
            for im in r.masses:
                im.extract_data()

            intgr_ranges = [(0.1, 0.2)] * len(r.masses)

            r.opt.show_img = True
            r._draw_mass(intgr_ranges)
            r._draw_signal(intgr_ranges)


