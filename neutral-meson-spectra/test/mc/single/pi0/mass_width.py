#!/usr/bin/python

from spectrum.spectrum import Spectrum, CompositeSpectrum
from spectrum.input import Input
from spectrum.options import Options
from spectrum.broot import BROOT as br
import spectrum.comparator as cmpr

import unittest
import operator

from test.mc.single.mass_width import MassWidthVerification 
from vault.datavault import DataVault
import unittest


class TestMassWidthPi0(MassWidthVerification, unittest.TestCase):

    def setUp(self):
        files_inputs = {
            DataVault().file("single #pi^{0}", "low"): (0, 7),
            DataVault().file("single #pi^{0}", "high"): (7, 20)
        } 
        self.shape_inputs = {
            Input(f, "PhysEffPlainOnlyTender", label="mc"): v 
            for f, v in files_inputs.iteritems()
        }

    def test_spectrum_shape(self):
        self.spectrum_shape(self.shape_inputs)

