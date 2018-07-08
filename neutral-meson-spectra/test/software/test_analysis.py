import unittest

from spectrum.output import AnalysisOutput
from spectrum.options import Options, CompositeOptions
from spectrum.analysis import Analysis
from vault.datavault import DataVault

# from spectrum.comparator import Comparator


class TestAnalysis(unittest.TestCase):

    # @unittest.skip('')
    def test_simple(self):
        analysis = Analysis(Options())

        output = analysis.transform(
            DataVault().input("data"),
            loggs=AnalysisOutput("test the single analysis")
        )
        self.assertGreater(len(output), 0)

    def test_composite(self):
        unified_inputs = {
            DataVault().input("single #pi^{0}", "low"): (0.0, 8.0),
            DataVault().input("single #pi^{0}", "high"): (4.0, 20.0)
        }

        analysis = Analysis(
            CompositeOptions(unified_inputs, "#pi^{0}")
        )

        output = analysis.transform(
            unified_inputs,
            loggs=AnalysisOutput("test the composite analysis")
        )
        # for o in output:
        #     Comparator().compare(o)
        self.assertGreater(len(output), 0)
