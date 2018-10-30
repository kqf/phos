import unittest
import pytest
from spectrum.pipeline import ComparePipeline
from spectrum.input import SingleHistInput
from spectrum.output import AnalysisOutput

from vault.datavault import DataVault


class TestPipeline(unittest.TestCase):

    @pytest.mark.onlylocal
    def test_comparator(self):
        estimator = ComparePipeline([
            ('normal', SingleHistInput("hPt_#pi^{0}_primary_")),
            ('normal', SingleHistInput("hPt_#pi^{0}_primary_standard")),
        ])

        loggs = AnalysisOutput("Testing the compare pipeline")
        output = estimator.transform(
            (DataVault().input("single #pi^{0}", "low"), ) * 2,
            loggs=loggs
        )
        self.assertGreater(output.GetEntries(), 0)
