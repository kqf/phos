import unittest
from vault.datavault import DataVault
from test.mc.single.spmc_efficiency import evaluate_spmc_efficiency

class TestEfficiencyEta(unittest.TestCase):

    def test_pi0_efficiency(self):
        unified_inputs = {
            DataVault().file("single #eta validate", "low"): (0, 6),
            DataVault().file("single #eta validate", "high"): (6, 20)
        }
        evaluate_spmc_efficiency(unified_inputs, "#eta")
  

