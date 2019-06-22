import ROOT
import json
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


@pytest.fixture
def data():
    return (
        DataVault().input("single #pi^{0}", "low", "PhysEff"),
        DataVault().input("single #pi^{0}", "low", "PhysEff"),
    )


@pytest.fixture
def empty_data(nhist=3):
    return (None, ) * nhist


@pytest.mark.onlylocal
def test_compares_single_inputs(data):
    estimator = ComparePipeline([
        ('normal1', SingleHistInput("hPt_#pi^{0}_primary_")),
        ('normal2', SingleHistInput("hPt_#pi^{0}_primary_standard")),
    ])

    loggs = AnalysisOutput("Test the compare pipeline")
    output = estimator.transform(
        data,
        loggs=loggs
    )
    loggs.plot()
    assert output.GetEntries() > 0


def test_compares_multiple(empty_data):
    estimator = ComparePipeline([
        ('normal{}'.format(i), MockInput("no option"))
        for i, _ in enumerate(empty_data)
    ])

    loggs = AnalysisOutput("Test the compare pipeline multiple")
    output = estimator.transform(
        empty_data,
        loggs=loggs
    )
    loggs.plot()
    assert output is None
