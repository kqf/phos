import unittest

from spectrum.efficiency import Efficiency, EfficiencyMultirange
from spectrum.comparator import Comparator
from spectrum.broot import BROOT as br
from vault.datavault import DataVault
from spectrum.input import Input
from spectrum.output import AnalysisOutput
from spectrum.options import EfficiencyOptions, MultirangeEfficiencyOptions


class TestEfficiency(unittest.TestCase):

    @unittest.skip("use the latest vault version")
    def test_interface(self):
        estimator = Efficiency(plot=False)
        efficiency = estimator.transform(
            DataVault().input("pythia8"),
            "test_efficeincy"
        )

        diff = Comparator()
        efficiency.SetTitle('Testing the interface')
        diff.compare(efficiency)


class TestMultirangeEfficiency(unittest.TestCase):

    def test_interface(self):
        unified_inputs = {
            DataVault().input("single #pi^{0}", "low"): (0, 7),
            DataVault().input("single #pi^{0}", "high"): (7, 20)
        }

        estimator = EfficiencyMultirange(
           MultirangeEfficiencyOptions.spmc(unified_inputs, "#pi^{0}")
        )

        efficiency = estimator.transform(
           unified_inputs,
           "testin composite efficiency"
        )

        efficiency.SetTitle('Testing the interface for composite efficency')
        diff = Comparator()
        diff.compare(efficiency)
