import unittest
import pytest

from spectrum.output import AnalysisOutput
from spectrum.options import Options, CompositeOptions
from spectrum.analysis import Analysis
from vault.datavault import DataVault

# from spectrum.comparator import Comparator


class TestAnalysis(unittest.TestCase):

    @unittest.skip('')
    @pytest.mark.onlylocal
    def test_simple(self):
        analysis = Analysis(Options())

        loggs = AnalysisOutput("test the single analysis")
        output = analysis.transform(
            DataVault().input("data"),
            loggs=loggs
        )
        loggs.plot()
        self.assertGreater(len(output), 0)

    @pytest.mark.onlylocal
    def test_composite(self):
        analysis = Analysis(CompositeOptions("#pi^{0}"))

        loggs = AnalysisOutput("test the composite analysis")
        output = analysis.transform(
            (
                DataVault().input("single #pi^{0}", "low", "PhysEff"),
                DataVault().input("single #pi^{0}", "high", "PhysEff"),
            ),
            loggs=loggs
        )
        loggs.plot()
        self.assertGreater(len(output), 0)
