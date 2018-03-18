import unittest

from spectrum.output import AnalysisOutput
from spectrum.analysis import CompositeAnalysis
from spectrum.options import CompositeOptions
from spectrum.comparator import Comparator
from spectrum.input import Input
from vault.datavault import DataVault


class TestCompositeSpectrum(unittest.TestCase):


   def test_interface(self):
        unified_inputs = {
            DataVault().input("single #pi^{0}", "low"): (0, 7),
            DataVault().input("single #pi^{0}", "high"): (7, 20)
        }

        analysis = CompositeAnalysis(
            CompositeOptions.spmc(unified_inputs, "#pi^{0}")
        )
        loggs = AnalysisOutput("test_the_composite_analysis_{0}".format("#pi^{0}"))
        output = analysis.transform(unified_inputs, loggs)
        loggs.update("final_result", output)
        loggs.plot()