#!/usr/bin/python

import unittest

from spectrum.spectrum import Spectrum, CompositeSpectrum
from spectrum.options import Options
from spectrum.input import Input
from spectrum.nonlinearity import Nonlinearity

import ROOT


class TestNonlinearity(unittest.TestCase):


    def _nonlinearity_function(self):
        func_nonlin = ROOT.TF1("func_nonlin", "[2] * (1.+[0]*TMath::Exp(-x/2*x/2/2./[1]/[1]))", 0, 100);
        func_nonlin.SetParNames('A', '#sigma', 'E_{scale}')
        func_nonlin.SetParameter(0, -0.05)
        func_nonlin.SetParameter(1, 0.6)
        func_nonlin.SetParLimits(1, 0, 10)
        func_nonlin.SetParameter(2, 1.04)
        return func_nonlin


    def test_nonlin_general(self):
        """
            Estimates nonlinearity parameters for General purpose MC
        """
        data = Spectrum(Input('LHC16', 'PhysOnlyTender', label='Data'), Options('d'))
        mc = Spectrum(Input('Pythia-LHC16-a5', 'PhysRawOnlyTender', label='R2D zs 20 MeV nonlin'), Options('d'))
        func = self._nonlinearity_function()

        nonlin = Nonlinearity(data, mc, func, mcname = 'pythia8')
        nonlin.evaluate_parameters()
