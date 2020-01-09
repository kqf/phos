import array
import pytest
import json


from spectrum.options import CompositeCorrectedYieldOptions
from spectrum.cyield import CorrectedYield
from spectrum.output import open_loggs
from spectrum.pipeline import ComparePipeline, Pipeline
from spectrum.pipeline import FunctionTransformer
from spectrum.pipeline import SingleHistReader
from spectrum.pipeline import TransformerBase
from spectrum.tools.feeddown import data_feeddown
import spectrum.broot as br
from spectrum.vault import DataVault


@pytest.fixture
def data():
    cyield = (
        (
            DataVault().input("data", histname="MassPtSM0"),
            data_feeddown(),
        ),
        (
            DataVault().input("single #pi^{0}", "low", "PhysEff"),
            DataVault().input("single #pi^{0}", "high", "PhysEff"),
        )
    )
    incnlo = DataVault().input("theory", "pythia6", histname="hxsPi0PtInv")
    return (cyield, incnlo)


class ErrorsTransformer(TransformerBase):
    def transform(self, data, loggs):
        for i in br.hrange(data):
            data.SetBinError(i, 0.0001)
        data.Sumw2()
        return data


class RebinTransformer(TransformerBase):
    def __init__(self, particle, filename):
        with open(filename) as f:
            self.edges = json.load(f)[particle]["ptedges"]

    def transform(self, hist, loggs):
        nbins = len(self.edges) - 1
        name = "{}_rebinned".format(hist.GetName())
        edges = array.array('d', self.edges)
        rebinned = hist.Rebin(nbins, name, edges)
        for i in br.hrange(rebinned):
            width = rebinned.GetBinWidth(i)
            rebinned.SetBinContent(i, rebinned.GetBinContent(i) / width)
        return rebinned


def normalize(hist, loggs):
    hist.Scale(1. / hist.Integral())
    return hist


def theory_prediction():
    pipeline = Pipeline([
        ("raw", SingleHistReader()),
        ("errors", ErrorsTransformer()),
        ("rebin", RebinTransformer("#pi^{0}", "config/pt-pythia6.json")),
        ("integral", FunctionTransformer(func=normalize)),
    ])
    return pipeline


def cyield(particle):
    ptfile = "config/pt-pythia6.json"
    options = CompositeCorrectedYieldOptions(particle=particle, pt=ptfile)
    return Pipeline([
        ("analysis", CorrectedYield(options)),
        ("integral", FunctionTransformer(func=normalize)),
    ])


@pytest.mark.onlylocal
@pytest.mark.interactive
def test_simple(data):
    estimator = ComparePipeline([
        ("data", cyield(particle="#pi^{0}")),
        ("pythia6", theory_prediction()),
    ], plot=True)

    with open_loggs() as loggs:
        estimator.transform(data, loggs=loggs)
