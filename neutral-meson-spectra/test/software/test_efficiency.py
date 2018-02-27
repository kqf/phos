import unittest

from spectrum.efficiency import Efficiency, EfficiencyMultirange
from spectrum.comparator import Comparator
from spectrum.broot import BROOT as br
from vault.datavault import DataVault
from spectrum.input import Input
from spectrum.output import AnalysisOutput
from spectrum.options import EfficiencyOptions, MultirangeEfficiencyOptions


class TestEfficiency(unittest.TestCase):

    # @unittest.skip("use the latest vault version")
    def test_interface(self):

        inputs = Input(
            DataVault().file("single #pi^{0} validate", "low"), 
            "PhysEff"
        )
        options = EfficiencyOptions()

        loggs = AnalysisOutput("test_efficiency", "#pi^{0}")

        estimator = Efficiency(options)
        efficiency = estimator.transform(inputs, loggs)
        efficiency.SetTitle('Testing the interface')

        diff = Comparator()
        diff.compare(efficiency)    

        loggs.plot(False)


class TestMultirangeEfficiency(unittest.TestCase):

    def test_interface(self):
        unified_inputs = {
            DataVault().file("single #pi^{0} validate", "low"): (0, 7),
            DataVault().file("single #pi^{0} validate", "high"): (7, 20)
        }

        estimator = EfficiencyMultirange(
           MultirangeEfficiencyOptions.spmc(unified_inputs) 
        )

        loggs = AnalysisOutput("test_multirange_efficiency", "#pi^{0}")

        efficiency = estimator.transform(
           [Input(filename, "PhysEff") for filename in unified_inputs],
           loggs
        )

        efficiency.SetTitle('Testing the interface')
        diff = Comparator()
        diff.compare(efficiency)
        loggs.plot(False)
        

  