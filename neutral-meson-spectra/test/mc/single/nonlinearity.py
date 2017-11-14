#!/usr/bin/python

import unittest

from spectrum.spectrum import Spectrum, CompositeSpectrum
from spectrum.options import Options
from spectrum.input import Input
from spectrum.nonlinearity import Nonlinearity

import ROOT


class TestNonlinearitySPMC(unittest.TestCase):

    def setUp(self):
        data = Spectrum(Input('LHC16', 'PhysOnlyTender'), Options('Data', 'd'))
        data = data.evaluate()
        self.data = data.mass


    def _nonlinearity_function(self):
        func_nonlin = ROOT.TF1("func_nonlin", "[2] * (1.+[0]*TMath::Exp(-x/2*x/2/2./[1]/[1]))", 0, 100);
        func_nonlin.SetParNames('A', '#sigma', 'E_{scale}')
        func_nonlin.SetParameter(0, -0.05)
        func_nonlin.SetParameter(1, 0.6)
        func_nonlin.SetParLimits(1, 0, 10)
        func_nonlin.SetParameter(2, 1.04)
        return func_nonlin


    def test_nonlin_spmc(self):
        """
            Estimates nonlinearity parameters for single-particle MC
        """
        inputs = {
            Input('/single/weight2/LHC17j3b1', 'PhysEffOnlyTender'): (0, 7), 
            Input('/single/weight2/LHC17j3b2', 'PhysEffOnlyTender'): (7, 20)
        }

        # NB: Mode doesn't apply here. It's overriten by single particle mc
        #

        spmc = CompositeSpectrum(inputs, Options('single particle mc'))
        spmc = spmc.evaluate()
        spmc = spmc.mass
        func = self._nonlinearity_function()

        nonlin = Nonlinearity(self.data, spmc, func, mcname = 'spmc')
        nonlin.evaluate_parameters()
