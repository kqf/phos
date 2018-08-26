import unittest
from vault.datavault import DataVault
from spectrum.options import CompositeCorrectedYieldOptions
from spectrum.output import AnalysisOutput
from uncertainties.gscale import GScale


class TestGeScaleUncertainty(unittest.TestCase):
    def test_interface_composite(self):
        unified_inputs = {
            DataVault().input("single #pi^{0}", "low"): (0, 7.0),
            DataVault().input("single #pi^{0}", "high"): (7.0, 20)
        }

        data = [
            DataVault().input("data"),
            unified_inputs
        ]

        estimator = GScale(
            CompositeCorrectedYieldOptions(
                particle="#pi^{0}",
                unified_inputs=unified_inputs
            ),
            plot=False
        )
        uncertanity = estimator.transform(
            data,
            loggs=AnalysisOutput("test composite corr. yield interface")
        )
