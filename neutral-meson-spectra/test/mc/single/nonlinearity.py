#!/usr/bin/python

import unittest

from vault.datavault import DataVault
from spectrum.options import CompositeNonlinearityOptions
from spectrum.output import AnalysisOutput
from tools.mc import Nonlinearity
from spectrum.broot import BROOT as br
from vault.formulas import FVault

import ROOT


def nonlinearity_function():
    func_nonlin = ROOT.TF1(
        "func_nonlin", FVault().func("nonlinearity"), 0, 5)
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

    def test_nonlin_photon_level(self):
        mcsel = "PhysNonlin2"
        selection = "PhysNonlinEst"
        histname = "MassPt_SM0"
        self.calculate(selection, mcsel, histname)

    def test_nonlin_pion_level(self):
        mcsel = "PhysEff2"
        selection = "Phys"
        histname = "MassPt"
        self.calculate(selection, mcsel, histname)

    def calculate(self, selection, mcsel, histname):
        unified_inputs = {
            DataVault().input("single #pi^{0} iteration d3 nonlin12", "low",
                              listname=mcsel,
                              histname=histname): (0, 7),
            DataVault().input("single #pi^{0} iteration d3 nonlin12", "high",
                              listname=mcsel,
                              histname=histname): (7, 20)
        }
        options = CompositeNonlinearityOptions(unified_inputs)
        options.fitf = nonlinearity_function()

        estimator = Nonlinearity(options, plot=True)
        nonlinearity = estimator.transform(
            [
                DataVault().input('data', listname=selection,
                                  histname=histname),
                unified_inputs
            ],
            loggs=AnalysisOutput("Testing the composite interface")
        )
        print "Fit parameters:", br.pars(options.fitf)
        self.assertGreater(nonlinearity.GetEntries(), 0)
