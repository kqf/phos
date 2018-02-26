import unittest

from spectrum.efficiency import Efficiency, EfficiencyMultirange
from spectrum.comparator import Comparator
from spectrum.broot import BROOT as br
from vault.datavault import DataVault
from spectrum.input import Input
from spectrum.output import AnalysisOutput


class TestEfficiency(unittest.TestCase):

    # @unittest.skip("use the latest vault version")
    def test_interface(self):

        inputs = Input(
            DataVault().file("single #pi^{0} validate", "low"), 
            "PhysEff"
        )

        loggs = AnalysisOutput("test_efficiency", "#pi^{0}")

        efficiency_estimator = Efficiency('hPt_#pi^{0}_primary_')
        efficiency = efficiency_estimator.transform(inputs, loggs)
        efficiency.SetTitle('Testing the interface')
        diff = Comparator()
        diff.compare(efficiency)    

        loggs.plot(False)


# class TestMultirangeEfficiency(unittest.TestCase):

#     def test_interface(self):
#         efficiency_estimator = EfficiencyMultirange(
#             'hPt_#pi^{0}_primary_', 
#             'eff',
#             {
#                 DataVault().file("single #pi^{0}", "low"): (0, 7),
#                 DataVault().file("single #pi^{0}", "high"): (7, 20)
#             }
#         )

#         efficiency = efficiency_estimator.eff()
#         efficiency.SetTitle('Testing the interface')

#         diff = Comparator()
#         diff.compare(efficiency)
        

#   