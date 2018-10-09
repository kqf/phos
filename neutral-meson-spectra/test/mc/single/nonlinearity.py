#!/usr/bin/python

import unittest

from vault.datavault import DataVault
from spectrum.options import CompositeNonlinearityOptions
from spectrum.output import AnalysisOutput
from tools.mc import Nonlinearity
from spectrum.broot import BROOT as br
# from vault.formulas import FVault

import ROOT


def nonlinearity_function():
    # func_nonlin = ROOT.TF1(
    #     "func_nonlin", FVault().func("nonlinearity"), 0, 20)
    # func_nonlin.SetParNames('A', '#sigma', 'E_{scale}')

    func_nonlin = ROOT.TF1(
        "func_nonlin",
        "[2]*(1.+[0]/(1. + TMath::Power(x/[1],2)))", 0, 100)
    func_nonlin.SetParameters(-0.06, 0.7, 1.015)
    return func_nonlin


class TestNonlinearitySPMC(unittest.TestCase):

    @unittest.skip("")
    def test_nonlin_photon_level(self):
        mcsel = "PhysNonlinPlain"
        selection = "PhysNonlinEst"
        histname = "MassPt_SM0"
        self.calculate(selection, mcsel, histname)

    def test_nonlin_pion_level(self):
        mcsel = "PhysEff"
        selection = "Phys"
        histname = "MassPt"
        self.calculate(selection, mcsel, histname)

    def calculate(self, selection, mcsel, hname):
        prod = "single #pi^{0} scan nonlinearity5"
        options = CompositeNonlinearityOptions()
        options.fitf = nonlinearity_function()

        estimator = Nonlinearity(options, plot=True)
        nonlinearity = estimator.transform(
            (
                DataVault().input('data', listname=selection, histname=hname),
                (
                    DataVault().input(prod, "low", mcsel, histname=hname),
                    DataVault().input(prod, "high", mcsel, histname=hname)
                )
            ),
            # loggs=AnalysisOutput("Testing the composite interface")
            "Testing the composite interface"
        )
        print "Fit parameters:", br.pars(options.fitf)
        self.assertGreater(nonlinearity.GetEntries(), 0)
