import unittest

# from spectrum.spectrum import Spectrum
from spectrum.input import Input
from spectrum.options import CorrectedYieldOptions
from spectrum.efficiency import Efficiency
from spectrum.corrected_yield import CorrectedYield
from spectrum.efficiency import EfficiencyMultirange

from spectrum.comparator import Comparator
from spectrum.broot import BROOT as br
from vault.datavault import DataVault


class TestCorrectedYield(unittest.TestCase):


    @unittest.skip('')
    def test_corrected_yield_for_pi0(self):
        unified_inputs = {
            DataVault().input("single #pi^{0} corrected weights", "low"):  (0, 7.0),
            DataVault().input("single #pi^{0} corrected weights", "high"): (7.0, 20)
        }

        data = [
            DataVault().input("data"),
            unified_inputs
        ]

        estimator = CorrectedYield(
            CorrectedYieldOptions(
                particle="#pi^{0}",
                unified_inputs=unified_inputs
            )
        )
        estimator.transform(data, "corrected yield #pi^{0}")


    # @unittest.skip('')
    def test_corrected_yield_for_eta(self):
        unified_inputs = {
            DataVault().input("single #eta updated", "low"):  (0, 6.0),
            DataVault().input("single #eta updated", "high"): (6.0, 20)
        }

        data = [
            DataVault().input("data"),
            unified_inputs
        ]

        estimator = CorrectedYield(
            CorrectedYieldOptions(
                particle="#eta",
                unified_inputs=unified_inputs
            )
        )
        estimator.transform(data, "corrected yield #eta")
