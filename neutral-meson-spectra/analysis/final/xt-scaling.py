import ROOT
import pytest
import json
import six
import numpy as np
import itertools

from spectrum.broot import BROOT as br
from spectrum.pipeline import TransformerBase, Pipeline
from spectrum.pipeline import ParallelPipeline
from spectrum.pipeline import ComparePipeline
from spectrum.output import open_loggs
from spectrum.comparator import Comparator


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
        xtedges = edges / (x.energy / 2)
        xt = ROOT.TH1F(
            "{}_xt".format(x.GetName()), x.GetTitle(),
            len(xtedges) - 1,
            xtedges)

        for i in br.range(x):
            xt.SetBinContent(i, x.GetBinContent(i))
            xt.SetBinError(i, x.GetBinError(i) * 0.0001)

        xt.logx = True
        xt.logy = True
        xt.label = str(x.energy)
        return xt


class ErrorsTransformer(TransformerBase):
    def transform(self, data, loggs):
        for i in br.range(data):
            data.SetBinError(i, 0.000001)
        # print(br.edges(data))
        return data


def xt(edges=None):
    return Pipeline([
        ("cyield", HepdataInput()),
        ("xt", XTtransformer())
    ])


@pytest.fixture(scope="module")
def data():
    with open("config/predictions/hepdata-pion.json") as f:
        data = json.load(f)
    labels, links = zip(*six.iteritems(data))
    steps = [(l, xt()) for l in labels]
    with open_loggs() as loggs:
        histograms = ParallelPipeline(steps).transform(links, loggs)
    return histograms


@pytest.mark.onlylocal
@pytest.mark.interactive
def test_xt_distribution(data):
    Comparator().compare(data)


# @pytest.mark.skip("")
@pytest.mark.onlylocal
@pytest.mark.interactive
def test_xt_scaling(data):
    for pair in itertools.combinations(data, 2):
        Comparator().compare(*pair)
