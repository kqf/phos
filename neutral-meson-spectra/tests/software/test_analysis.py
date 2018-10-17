import unittest
import pytest

from spectrum.output import AnalysisOutput
from spectrum.options import Options, CompositeOptions
from spectrum.analysis import Analysis
from vault.datavault import DataVault

# from spectrum.comparator import Comparator


class TestAnalysis(unittest.TestCase):

    # @unittest.skip('')
    @pytest.mark.onlylocal
    def test_simple(self):
        analysis = Analysis(Options())

        output = analysis.transform(
            DataVault().input("data"),
            loggs=AnalysisOutput("test the single analysis")
        )
        self.assertGreater(len(output), 0)

    @pytest.mark.onlylocal
    def test_composite(self):
        analysis = Analysis(CompositeOptions("#pi^{0}"))

        output = analysis.transform(
            (
                DataVault().input("single #pi^{0}", "low"),
                DataVault().input("single #pi^{0}", "high"),
            ),
            loggs=AnalysisOutput("test the composite analysis")
        )
        self.assertGreater(len(output), 0)
