#!/usr/bin/python

import unittest

from vault.datavault import DataVault
from spectrum.options import CompositeNonlinearityOptions
from spectrum.output import AnalysisOutput
from tools.mc import Nonlinearity
from spectrum.broot import BROOT as br

import ROOT


def nonlinearity_function():
    func_nonlin = ROOT.TF1(
        "func_nonlin", "[2] * (1.+[0]*TMath::Exp(-x*x/2./[1]/[1]))", 0, 20)
    func_nonlin.SetParNames('A', '#sigma', 'E_{scale}')
    # func_nonlin.SetParameters(-0.014719244288611932,
    # 0.8017501954719543, 1.050000000000015)
    func_nonlin.SetParameter(0, -0.014719244288611932)
    func_nonlin.SetParameter(1, 0.8017501954719543 * 2)
    func_nonlin.SetParameter(2, 1.050000000000015)
    # func_nonlin.SetParameter(0, -0.01)
    # func_nonlin.SetParameter(1, 1.12)
    # func_nonlin.FixParameter(2, 1.06)

    # func_nonlin.SetParLimits(0, -10, -0.001)
    # func_nonlin.SetParLimits(1, 0, 1.12)
    # func_nonlin.SetParLimits(2, 1.05, 1.09)
    return func_nonlin


class TestNonlinearitySPMC(unittest.TestCase):

    def test_composite(self):
        unified_inputs = {
            DataVault().input("single #pi^{0} iteration d3 test1", "low",
                              listname="PhysEffPlain",
                              histname="MassPt"): (0, 7),
            DataVault().input("single #pi^{0} iteration d3 test1", "high",
                              listname="PhysEffPlain",
                              histname="MassPt"): (7, 20)
        }
        options = CompositeNonlinearityOptions(unified_inputs)
        options.fitf = nonlinearity_function()

        estimator = Nonlinearity(options)
        nonlinearity = estimator.transform(
            [
                DataVault().input('data', listname="Phys",
                                  histname='MassPt'),
                unified_inputs
            ],
            loggs=AnalysisOutput("Testing the composite interface")
        )
        print "Fit parameters:", br.pars(options.fitf)
        self.assertGreater(nonlinearity.GetEntries(), 0)
