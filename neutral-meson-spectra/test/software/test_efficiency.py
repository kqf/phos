import unittest

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

    def test_composite(self):
        unified_inputs = {
            DataVault().input("single #pi^{0}", "low"): (0, 7),
            DataVault().input("single #pi^{0}", "high"): (7, 20)
        }

        estimator = Efficiency(
            CompositeEfficiencyOptions.spmc(unified_inputs, "#pi^{0}")
        )

        efficiency = estimator.transform(
            unified_inputs,
            "testin composite efficiency"
        )
        self.assertGreater(efficiency.GetEntries(), 0)
