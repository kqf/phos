#!/usr/bin/python

from spectrum.spectrum import Spectrum, CompositeSpectrum
from spectrum.input import Input
from spectrum.options import Options
from spectrum.broot import BROOT as br
import spectrum.comparator as cmpr

import unittest
import operator

from test.mc.single.mass_width import TestMassWidth


class TestMassWidthPi0(TestMassWidth):

    def setUp(self):
        ddir = '/single/weight2/'
        files = {
                    ddir + 'LHC17j3b1': (0, 6),
                    ddir + 'LHC17j3b2': (9, 20)
        }

        inputs = [Input(f, 'PhysEffOnlyTender', label='#pi0') for f in files]
        options = [Options.spmc(rr) for f, rr in files.iteritems()]
        f = lambda x, y: Spectrum(x, y).evaluate()
        self.results = map(f, inputs, options)

        self.shape_inputs = {
            Input(ddir + 'LHC17j3b1', 'PhysEffOnlyTender'): (0, 7), 
            Input(ddir + 'LHC17j3b2', 'PhysEffOnlyTender'): (7, 20)
        }

