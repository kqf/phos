#!/usr/bin/python

from spectrum.spectrum import Spectrum, CompositeSpectrum
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

        inputs = [Input(f, 'PhysEffOnlyTender') for f in files]
        inputs = map(operator.methodcaller('read'), inputs)

        options = [Options.spmc(rr, particle='eta') for f, rr in files.iteritems()]
        f = lambda x, y: Spectrum(x, y).evaluate()
        self.results = map(f, inputs, options)



    def test_different_mc_productions(self):
        masses, widths = zip(*self.results)[0:2]

        indata, doptions = Input('uncorrected/LHC16', 'EtaTender'), Options('data', particle='eta')
        dmass, dwidth = Spectrum(indata, doptions).evaluate()[0:2]

        diff = cmpr.Comparator((0.5, 1.), rrange = (0, 2),
                        # crange=(0.4, 0.5), 
                        oname = 'compared-spmc-masses')
        diff.compare(list(masses) + [dmass])

        diff = cmpr.Comparator((0.5, 1.), rrange = (0, 2),
                        crange=(0.0, 0.02), oname = 'compared-spmc-widths')
        diff.compare(list(widths) + [dwidth])
