import unittest
import pytest
import ROOT

from vault.datavault import DataVault
from spectrum.options import NonlinearityOptions, CompositeNonlinearityOptions
from spectrum.output import AnalysisOutput
from tools.mc import Nonlinearity


def nonlinearity_function():
    func_nonlin = ROOT.TF1(
        "func_nonlin",
        "[2] * (1.+[0]*TMath::Exp(-x/2*x/2/2./[1]/[1]))",
        0, 100
    )
    func_nonlin.SetParNames("A", "#sigma", "E_{scale}")
    func_nonlin.SetParameter(0, -0.05)
    func_nonlin.SetParameter(1, 0.6)
    func_nonlin.SetParLimits(1, 0, 10)
    func_nonlin.SetParameter(2, 1.04)
    return func_nonlin


class TestNonlinearityEstimator(unittest.TestCase):

    @pytest.mark.skip("The datafile is missing")
    @pytest.mark.onlylocal
    def test_simple(self):
        options = NonlinearityOptions()
        options.fitf = nonlinearity_function()

        estimator = Nonlinearity(options)
        nonlinearity = estimator.transform(
            (
                DataVault().input("data", listname="PhysNonlinEst",
                                  histname="MassPt_SM0"),
                DataVault().input("pythia8", listname="PhysNonlin",
                                  histname="MassPt_SM0"),
            ),
            loggs=AnalysisOutput("Testing the interface")
        )
        self.assertGreater(nonlinearity.GetEntries(), 0)

    @pytest.mark.skip("The datafile is missing")
    @pytest.mark.onlylocal
    def test_composite(self):
        options = CompositeNonlinearityOptions()
        options.fitf = nonlinearity_function()

        estimator = Nonlinearity(options)
        hist = "MassPt_SM0"
        nonlinearity = estimator.transform(
            (
                DataVault().input("data", listname="PhysNonlinEst",
                                  histname=hist),
                (
                    DataVault().input(
                        "single #pi^{0}", "low", "PhysNonlin", histname=hist),
                    DataVault().input(
                        "single #pi^{0}", "high", "PhysNonlin", histname=hist)
                )
            ),
            loggs=AnalysisOutput("Testing the composite interface")
        )
        self.assertGreater(nonlinearity.GetEntries(), 0)
