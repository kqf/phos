import ROOT
import json
import unittest
import pytest
from spectrum.pipeline import TransformerBase
from spectrum.pipeline import ComparePipeline
from spectrum.input import SingleHistInput
from spectrum.output import AnalysisOutput
import array


from vault.datavault import DataVault


class MockInput(TransformerBase):
    def transform(self, data, loggs):
        with open('config/pt.json') as f:
            pt = json.load(f)["#pi^{0}"]["ptedges"]
        out = ROOT.TH1F("mock", "Input", len(pt) - 1, array.array('d', pt))
        out.FillRandom("pol0", 10000)
        loggs.update({"input": out})
        return out


class TestComparePipelineWithRatio(unittest.TestCase):
    @pytest.mark.onlylocal
    def test_compares_single_inputs(self):
        estimator = ComparePipeline([
            ('normal1', SingleHistInput("hPt_#pi^{0}_primary_")),
            ('normal2', SingleHistInput("hPt_#pi^{0}_primary_standard")),
        ])

        loggs = AnalysisOutput("Test the compare pipeline")
        output = estimator.transform(
            (DataVault().input("single #pi^{0}", "low", "PhysEff"), ) * 2,
            loggs=loggs
        )
        loggs.plot()
        self.assertGreater(output.GetEntries(), 0)

    def test_compares_multiple(self, nhist=3):
        estimator = ComparePipeline([
            ('normal{}'.format(i), MockInput("no option"))
            for i in range(nhist)
        ])

        loggs = AnalysisOutput("Test the compare pipeline multiple")
        output = estimator.transform(
            (None, ) * nhist,
            loggs=loggs
        )
        loggs.plot()
        self.assertIsNone(output)
