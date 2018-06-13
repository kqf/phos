import unittest

from spectrum.options import CompositeCorrectedYieldOptions
from spectrum.corrected_yield import CorrectedYield

from vault.datavault import DataVault


class TestCorrectedYield(unittest.TestCase):

    @unittest.skip('')
    def test_corrected_yield_for_pi0(self):
        # production = "single #pi^{0} iteration3 yield aliphysics"
        production = "single #pi^{0} iteration d3 nonlin14"
        unified_inputs = {
            DataVault().input(production, "low"): (0, 8.0),
            DataVault().input(production, "high"): (4.0, 20)
        }

        data = [
            DataVault().input("data"),
            unified_inputs
        ]

        estimator = CorrectedYield(
            CompositeCorrectedYieldOptions(
                particle="#pi^{0}",
                unified_inputs=unified_inputs
            )
        )
        estimator.transform(data, "corrected yield #pi^{0}")

    # @unittest.skip('')
    def test_corrected_yield_for_eta(self):
        production = "single #eta new tender"
        unified_inputs = {
            DataVault().input(production, "low"): (0, 10),
            DataVault().input(production, "high"): (4.0, 20)
        }

        data = [
            DataVault().input("data"),
            unified_inputs
        ]

        estimator = CorrectedYield(
            CompositeCorrectedYieldOptions(
                particle="#eta",
                unified_inputs=unified_inputs
            )
        )
        estimator.transform(data, "corrected yield #eta")
