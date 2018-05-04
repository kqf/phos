import unittest
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
    func_nonlin.SetParNames('A', '#sigma', 'E_{scale}')
    func_nonlin.SetParameter(0, -0.05)
    func_nonlin.SetParameter(1, 0.6)
    func_nonlin.SetParLimits(1, 0, 10)
    func_nonlin.SetParameter(2, 1.04)
    return func_nonlin


class TestNonlinearityEstimator(unittest.TestCase):

    def test_simple(self):
        options = NonlinearityOptions()
        options.fitf = nonlinearity_function()

        estimator = Nonlinearity(options)
        nonlinearity = estimator.transform(
            [
                DataVault().input('data', listname="PhysNonlinEst",
                                  histname='MassPt_SM0'),
                DataVault().input('pythia8', listname="PhysNonlinTender",
                                  histname='MassPt_SM0'),
            ],
            loggs=AnalysisOutput("Testing the interface")
        )
        self.assertGreater(nonlinearity.GetEntries(), 0)

    def test_composite(self):
        unified_inputs = {
            DataVault().input("single #pi^{0}", "low",
                              listname="PhysNonlin",
                              histname="MassPt_SM0"): (0, 7),
            DataVault().input("single #pi^{0}", "high",
                              listname="PhysNonlin",
                              histname="MassPt_SM0"): (7, 20)
        }
        options = CompositeNonlinearityOptions(unified_inputs)
        options.fitf = nonlinearity_function()

        estimator = Nonlinearity(options)
        nonlinearity = estimator.transform(
            [
                DataVault().input('data', listname="PhysNonlinEst",
                                  histname='MassPt_SM0'),
                unified_inputs
            ],
            loggs=AnalysisOutput("Testing the composite interface")
        )
        self.assertGreater(nonlinearity.GetEntries(), 0)
