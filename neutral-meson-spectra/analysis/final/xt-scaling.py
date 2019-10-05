import ROOT
import pytest
import json
import six
import numpy as np
import itertools

from spectrum.broot import BROOT as br
from spectrum.pipeline import TransformerBase, Pipeline
from spectrum.pipeline import ParallelPipeline
from spectrum.comparator import Comparator
from spectrum.output import open_loggs
from vault.formulas import FVault


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
            xt.SetBinError(i, x.GetBinError(i) / 2)

        xt.logx = True
        xt.logy = True
        xt.label = str(x.energy)
        xt.energy = x.energy
        xt.fitfunc = x.fitfunc
        return xt


class DataFitter(TransformerBase):
    def transform(self, x, loggs):
        tsallis = FVault().tf1("tsallis")
        x.Fit(tsallis, "R")
        x.fitfunc = tsallis
        return x


class ErrorsTransformer(TransformerBase):
    def transform(self, data, loggs):
        for i in br.range(data):
            data.SetBinError(i, 0.000001)
        return data


def xt(edges=None):
    return Pipeline([
        ("cyield", HepdataInput()),
        ("fit", DataFitter()),
        ("xt", XTtransformer()),
    ])


def n_factor(hist1, hist2):
    nxt = hist1.Clone("n")
    nxt.Divide(br.function2histogram(hist2.fitfunc, nxt, hist2.energy / 2))
    contents, errors, centers = br.bins(nxt)
    logcontents = - np.log(contents) / np.log(hist1.energy / hist2.energy)
    logerrors = errors / contents
    for (i, c, e) in zip(br.range(nxt), logcontents, logerrors):
        nxt.SetBinContent(i, c)
        # nxt.SetBinError(i, e)
    nxt.label = "{} {}".format(hist1.label, hist2.label)
    return nxt


@pytest.fixture(scope="module")
def data():
    with open("config/predictions/hepdata-pion.json") as f:
        data = json.load(f)
    labels, links = zip(*six.iteritems(data))
    steps = [(l, xt()) for l in labels]
    with open_loggs() as loggs:
        histograms = ParallelPipeline(steps).transform(links, loggs)
    return histograms


@pytest.mark.skip("")
@pytest.mark.onlylocal
@pytest.mark.interactive
def test_xt_distribution(data):
    Comparator().compare(data)


@pytest.mark.onlylocal
@pytest.mark.interactive
def test_xt_scaling(data):
    spectra = sorted(data, key=lambda x: x.energy)
    n_factors = [n_factor(*pair)
                 for pair in itertools.combinations(spectra, 2)]
    Comparator().compare(n_factors)
