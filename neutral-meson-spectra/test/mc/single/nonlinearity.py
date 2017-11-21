#!/usr/bin/python

import unittest

from spectrum.spectrum import Spectrum, CompositeSpectrum
from spectrum.options import Options
from spectrum.input import Input
from spectrum.nonlinearity import Nonlinearity

import ROOT


class TestNonlinearitySPMC(unittest.TestCase):

    def _nonlinearity_function(self):
        func_nonlin = ROOT.TF1("func_nonlin", "[2] * (1.+[0]*TMath::Exp(-x/2*x/2/2./[1]/[1]))", 0, 100);
        func_nonlin.SetParNames('A', '#sigma', 'E_{scale}')
        # func_nonlin.SetParameters(-0.020071867975567686, 1.1184319273953713, 1.049371977284965)
        func_nonlin.SetParameter(0, -0.05)
        func_nonlin.SetParameter(1, 0.6)
        func_nonlin.FixParameter(2, 1.05)
        func_nonlin.SetParLimits(0, -10, -0.001)
        func_nonlin.SetParLimits(1, 0, 1.12)
        # func_nonlin.SetParLimits(2, 0, 1.08)
        return func_nonlin


    def test_nonlin_spmc(self):
        """
            Estimates nonlinearity parameters for single-particle MC
        """
        data = Spectrum(Input('LHC16', 'PhysOnlyTender'), Options('data', 'd'))


        inputs = {
            Input('/single/weight2/LHC17j3b1', 'PhysEffOnlyTender'): (0, 7), 
            Input('/single/weight2/LHC17j3b2', 'PhysEffOnlyTender'): (7, 20)
        }

        # NB: Mode doesn't apply here. It's overriten by single particle mc
        #

        spmc = CompositeSpectrum(inputs, Options('single particle mc'))
        func = self._nonlinearity_function()
        nonlin = Nonlinearity(data, spmc, func, mcname = 'spmc')
        nonlin.evaluate_parameters()
