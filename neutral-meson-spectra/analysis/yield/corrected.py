import unittest

from spectrum.options import CompositeCorrectedYieldOptions
from spectrum.corrected_yield import CorrectedYield

from vault.datavault import DataVault


class TestCorrectedYield(unittest.TestCase):

    # @unittest.skip('')
    def test_corrected_yield_for_pi0(self):
        unified_inputs = {
            DataVault().input("single #pi^{0} iteration3 yield aliphysics", "low"): (0, 7.0),
            DataVault().input("single #pi^{0} iteration3 yield aliphysics", "high"): (7.0, 20)
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

    @unittest.skip('')
    def test_corrected_yield_for_eta(self):
        unified_inputs = {
            DataVault().input("single #eta new tender", "low"): (0, 6.0),
            DataVault().input("single #eta new tender", "high"): (6.0, 20)
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
