#!/usr/bin/python

import unittest

from spectrum.spectrum import Spectrum, CompositeSpectrum
from spectrum.options import Options
from spectrum.input import Input
from spectrum.nonlinearity import Nonlinearity

import ROOT


class TestNonlinearitySPMC(unittest.TestCase):

    def _nonlinearity_function(self):
        func_nonlin = ROOT.TF1("func_nonlin", "[2] * (1.+[0]*TMath::Exp(-x*x/2./[1]/[1]))", 0, 20)
        func_nonlin.SetParNames('A', '#sigma', 'E_{scale}')
        # func_nonlin.SetParameters(-0.014719244288611932, 0.8017501954719543, 1.050000000000015)
        func_nonlin.FixParameter(0, -0.014719244288611932)
        func_nonlin.FixParameter(1, 0.8017501954719543 * 2)
        func_nonlin.FixParameter(2, 1.050000000000015)
        # func_nonlin.SetParameter(0, -0.01)
        # func_nonlin.SetParameter(1, 1.12)
        # func_nonlin.FixParameter(2, 1.06)

        # func_nonlin.SetParLimits(0, -10, -0.001)
        # func_nonlin.SetParLimits(1, 0, 1.12)
        # func_nonlin.SetParLimits(2, 1.05, 1.09)
        return func_nonlin


    def test_nonlin_spmc(self):
        """
            Estimates nonlinearity parameters for single-particle MC
        """
        data = Spectrum(Input('uncorrected/LHC16', 'PhysNonlinEstTender', 'MassPt_SM0', label='data'), 
                        Options('d'))


        mclabel = 'single particle mc'
        inputs = {
            Input('/single/nonlin0/LHC17j3b1', 'PhysNonlinTender', 'MassPt_SM0', label=mclabel): (0, 5.5), 
            Input('/single/nonlin0/LHC17j3b2', 'PhysNonlinTender', 'MassPt_SM0', label=mclabel): (5.5, 20)
        }

        # NB: Mode doesn't apply here. It's overriten by single particle mc
        #

        spmc = CompositeSpectrum(inputs)
        func = self._nonlinearity_function()
        nonlin = Nonlinearity(data, spmc, func, mcname = 'spmc')
        nonlin.evaluate_parameters()
