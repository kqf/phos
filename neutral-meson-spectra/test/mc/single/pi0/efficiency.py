import unittest

from vault.datavault import DataVault
from test.mc.single.spmc_efficiency import evaluate_spmc_efficiency

class TestEfficiencyPi0(unittest.TestCase):

    def test_pi0_efficiency(self):
        unified_inputs = {
            DataVault().file("single #pi^{0}", "low"): (0, 7),
            DataVault().file("single #pi^{0}", "high"): (7, 20)
        }
        evaluate_spmc_efficiency(unified_inputs, "#pi^{0}")
  