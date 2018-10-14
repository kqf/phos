import unittest
import pytest

from spectrum.efficiency import Efficiency
from vault.datavault import DataVault
from spectrum.options import EfficiencyOptions, CompositeEfficiencyOptions


class TestEfficiency(unittest.TestCase):

    @unittest.skip('')
    def test_simple(self):
        estimator = Efficiency(
            EfficiencyOptions(genname='hPt_#pi^{0}_primary_'),
            plot=False
        )

        efficiency = estimator.transform(
            DataVault().input("pythia8"),
            "test_efficeincy"
        )
        self.assertGreater(efficiency.GetEntries(), 0)

    @pytest.mark.onlylocal
    def test_composite(self):
        estimator = Efficiency(CompositeEfficiencyOptions("#pi^{0}"))
        efficiency = estimator.transform(
            [
                DataVault().input("single #pi^{0}", "low"),
                DataVault().input("single #pi^{0}", "high"),
            ],
            "testing composite efficiency"
        )
        self.assertGreater(efficiency.GetEntries(), 0)
