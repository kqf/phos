import ROOT
import pytest
import json
import six
import numpy as np

from spectrum.broot import BROOT as br
from spectrum.pipeline import TransformerBase, Pipeline
from spectrum.pipeline import ComparePipeline
from spectrum.output import open_loggs
from spectrum.input import SingleHistInput

from vault.datavault import DataVault


class HepdataInput(TransformerBase):
    def __init__(self, table_name="Table 1", histname="Hist1D_y1", plot=False):
        super(HepdataInput, self).__init__(plot)
        self.histname = histname

    def transform(self, item, loggs):
        filename = ".hepdata-cachedir/{}".format(item["file"])
        br.io.hepdata(item["hepdata"], filename, item["table"])
        hist = br.io.read(filename, item["table"], self.histname)
        hist.logy = True
        hist.logx = False
        hist.Scale(item["scale"])
        hist.energy = item["energy"]
        return hist


class XTtransformer(TransformerBase):
    def transform(self, x, loggs):
        edges = np.array([x.GetBinLowEdge(i) for i in br.range(x, edges=True)])
        xtedges = edges / x.energy
        xt = ROOT.TH1F(
            "{}_xt".format(x.GetName()), x.GetTitle(),
            len(xtedges) - 1,
            xtedges)

        for i in br.range(x):
            xt.SetBinContent(i, x.GetBinContent(i))
            xt.SetBinError(i, x.GetBinContent(i) * 0.0001)
        xt.Scale(x.energy)
        xt.logx = True
        xt.logy = True
        return xt


class ErrorsTransformer(TransformerBase):
    def transform(self, data, loggs):
        for i in br.range(data):
            data.SetBinError(i, 0.0001)
        data.Sumw2()
        return data


def theory_prediction(label):
    pipeline = Pipeline([
        ("raw", SingleHistInput("#sigma_{total}")),
        ("errors", ErrorsTransformer())
    ])
    return (label, pipeline)


@pytest.fixture
def datasets():
    with open("config/different-energies.json") as f:
        data = json.load(f)
    labels, links = zip(*six.iteritems(data))
    steps = [(l, HepdataInput()) for l in labels]
    return steps, links


@pytest.fixture
def incnlo_datasets(datasets):
    steps, links = datasets
    steps.append(theory_prediction("INCNLO 13 TeV"))
    steps.append(theory_prediction("INCNLO 7 TeV"))
    links = list(links)
    links.append(DataVault().input("theory", "incnlo"))
    links.append(DataVault().input("theory", "7 TeV"))
    return steps, links


@pytest.mark.skip("")
@pytest.mark.onlylocal
@pytest.mark.interactive
def test_downloads_from_hepdata(datasets):
    steps, links = datasets
    with open_loggs() as loggs:
        ComparePipeline(steps, plot=True).transform(links, loggs)


@pytest.fixture
def xtdatasets():
    def xt():
        return Pipeline([
            ("cyield", HepdataInput()),
            ("cyield", XTtransformer()),
        ])
    with open("config/different-energies.json") as f:
        data = json.load(f)
    labels, links = zip(*six.iteritems(data))
    steps = [(l, xt()) for l in labels]
    return steps, links


# @pytest.mark.skip("")
@pytest.mark.onlylocal
@pytest.mark.interactive
def test_xt_distribution(xtdatasets):
    steps, links = xtdatasets
    with open_loggs("compare yields") as loggs:
        ComparePipeline(steps, plot=True).transform(links, loggs)
