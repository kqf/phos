import unittest

from spectrum.options import CompositeCorrectedYieldOptions
from spectrum.corrected_yield import CorrectedYield

from vault.datavault import DataVault
from tools.feeddown import data_feeddown


class TestCorrectedYield(unittest.TestCase):

    # @unittest.skip('')
    def test_corrected_yield_for_pi0(self):
        production = "single #pi^{0}"
        inputs = (
            DataVault().input(production, "low", "PhysEff"),
            DataVault().input(production, "high", "PhysEff"),
        )
        yield_data = (
            DataVault().input("data"),
            data_feeddown(),
        )
        data = (
            yield_data,
            inputs
        )

        estimator = CorrectedYield(
            CompositeCorrectedYieldOptions(
                particle="#pi^{0}"
            )
        )
        estimator.transform(data, "corrected yield #pi^{0}")

    @unittest.skip('')
    def test_corrected_yield_for_eta(self):
        production = "single #eta new tender"
        inputs = (
            DataVault().input(production, "low"),
            DataVault().input(production, "high"),
        )

        data = (
            DataVault().input("data"),
            inputs
        )

        estimator = CorrectedYield(
            CompositeCorrectedYieldOptions(particle="#eta")
        )
        estimator.transform(data, "corrected yield #eta")
