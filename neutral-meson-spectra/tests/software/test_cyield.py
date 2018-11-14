import unittest
import pytest

from spectrum.options import CompositeCorrectedYieldOptions
from spectrum.options import CorrectedYieldOptions
from spectrum.corrected_yield import CorrectedYield

from vault.datavault import DataVault
from tools.feeddown import data_feeddown


class TestCorrectedYieldInterface(unittest.TestCase):

    @pytest.mark.onlylocal
    def test_yield(self):
        yield_data = (
            DataVault().input("data"),
            data_feeddown(),
        )
        data = (
            yield_data,
            DataVault().input("pythia8"),
        )

        estimator = CorrectedYield(
            CorrectedYieldOptions(
                particle="#pi^{0}"
            )
        )
        estimator.transform(data, {})

    @pytest.mark.onlylocal
    def test_composite_yield(self):
        production = "single #pi^{0}"
        spmc_inputs = (
            DataVault().input(production, "low", "PhysEff"),
            DataVault().input(production, "high", "PhysEff"),
        )
        yield_data = (
            DataVault().input("data"),
            data_feeddown(),
        )
        data = (
            yield_data,
            spmc_inputs
        )

        estimator = CorrectedYield(
            CompositeCorrectedYieldOptions(
                particle="#pi^{0}"
            )
        )
        estimator.transform(data, {})
