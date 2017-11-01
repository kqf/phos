#!/usr/bin/python

import unittest

from spectrum.spectrum import Spectrum, CompositeSpectrum
from spectrum.options import Options
from spectrum.input import Input
from spectrum.nonlinearity import Nonlinearity

import ROOT


class TestNonlinearity(unittest.TestCase):

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


    @unittest.skip('')
    def test_nonlin_general(self):
        """
            Estimates nonlinearity parameters for General purpose MC
        """
        mc = Spectrum(Input('Pythia-LHC16-a5', 'PhysRawOnlyTender'), Options('R2D zs 20 MeV nonlin', 'd'))
        mc = mc.evaluate()
        mc = mc.mass
        func = self._nonlinearity_function()
        nonlin = Nonlinearity(self.data, mc, func, mcname = 'pythia8')
        nonlin.evaluate_parameters()


    def test_nonlin_spmc(self):
        """
            Estimates nonlinearity parameters for single-particle MC
        """
        inputs = {
            Input('/single/plain/scaled-LHC17j3b1', 'MCStudyOnlyTender'): (0, 7), 
            Input('/single/plain/scaled-LHC17j3b2', 'MCStudyOnlyTender'): (7, 20)
        }

        spmc = CompositeSpectrum(inputs, Options('single particle mc', mode = 'd'))
        spmc = spmc.evaluate()
        spmc = spmc.mass
        func = self._nonlinearity_function()

        nonlin = Nonlinearity(self.data, spmc, func, mcname = 'spmc')
        nonlin.evaluate_parameters()
