import unittest

# from spectrum.spectrum import Spectrum
from spectrum.corrected_yield import CorrectedYield
from spectrum.options import CorrectedYieldOptions

from vault.datavault import DataVault


class TestCorrectedYield(unittest.TestCase):


    def test_interface_simple(self):
        data = [
            DataVault().input("data"),
            DataVault().input("pythia8")
        ]

        estimator = CorrectedYield()
        estimator.transform(data, "test simple corr. yield interface")

    def test_interface_composite(self):
        unified_inputs = {
            DataVault().input("single #pi^{0}", "low"):  (0, 7.0),
            DataVault().input("single #pi^{0}", "high"): (7.0, 20)
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
        estimator.transform(data, "test composite corr. yield interface")
