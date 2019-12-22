import array
import ROOT
import pytest
import json
import six
import numpy as np

import spectrum.broot as br
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
        edges = np.array([
            x.GetBinLowEdge(i)
            for i in br.hrange(x, edges=True)])
        xtedges = edges / x.energy
        xt = ROOT.TH1F(
            "{}_xt".format(x.GetName()), x.GetTitle(),
            len(xtedges) - 1,
            xtedges)

        for i in br.hrange(x):
            xt.SetBinContent(i, x.GetBinContent(i))
            xt.SetBinError(i, x.GetBinContent(i) * 0.0001)
        # xt.Scale(x.nergy)
        xt.logx = True
        xt.logy = True
        return xt


def scale_bin_width(hist, rebins=None):
    hist = hist.Clone()
    width = 1
    for i in br.hrange(hist):
        if rebins is not None:
            width = rebins[i - 1] + 1
        hist.SetBinContent(i, hist.GetBinContent(i) / width)
    return hist


def meregd_bins(new, old):
    new, old = br.edges(new), br.edges(old)

    def nbins(a, b):
        return [pT for pT in old if a < pT < b]

    rebins = [len(nbins(*edge)) for edge in zip(new[:-1], new[1:])]
    return rebins


class RebinTransformer(TransformerBase):
    def __init__(self, edges=None):
        self.edges = edges

    def transform(self, hist, loggs):
        if not self.edges:
            return hist

        nbins = len(self.edges) - 1
        name = "{}_rebinned".format(hist.GetName())
        edges = array.array('d', self.edges)
        rebinned = hist.Rebin(nbins, name, edges)
        rebins = meregd_bins(rebinned, hist)
        rebinned = scale_bin_width(rebinned, rebins)
        rebinned.energy = hist.energy
        rebinned.logy = True
        return rebinned


class ErrorsTransformer(TransformerBase):
    def transform(self, data, loggs):
        for i in br.hrange(data):
            data.SetBinError(i, 0.000001)
        # print(br.edges(data))
        return data


def hepdata():
    return Pipeline([
        ("raw", HepdataInput()),
        ("errors", ErrorsTransformer()),
    ])


def xt(edges=None):
    return Pipeline([
        ("cyield", HepdataInput()),
        ("rebin", RebinTransformer(edges=edges)),
        ("errors", ErrorsTransformer()),
    ])


def theory_prediction():
    pipeline = Pipeline([
        ("raw", SingleHistInput("#sigma_{total}")),
        ("errors", ErrorsTransformer())
    ])
    return pipeline


@pytest.fixture
def data():
    with open("config/predictions/hepdata-pion.json") as f:
        data = json.load(f)
    return data


# @pytest.mark.skip("")
@pytest.mark.onlylocal
@pytest.mark.interactive
def test_downloads_from_hepdata(data):
    labels, links = zip(*six.iteritems(data))
    steps = [(l, hepdata()) for l in labels]
    steps.append(("incnlo", theory_prediction()))
    links = list(links)
    links.append(DataVault().input("theory", "7 TeV"))
    with open_loggs() as loggs:
        ComparePipeline(steps, plot=True).transform(links, loggs)


@pytest.mark.skip("")
@pytest.mark.onlylocal
@pytest.mark.interactive
def test_xt_distribution(data):
    labels, links = zip(*six.iteritems(data))
    steps = [(l, xt()) for l in labels]
    with open_loggs("compare yields") as loggs:
        ComparePipeline(steps, plot=True).transform(links, loggs)


@pytest.fixture
def xt_scaling_pairs():
    with open("config/predictions/same-binning.json") as f:
        data = json.load(f)
    return data


@pytest.mark.skip("")
@pytest.mark.onlylocal
@pytest.mark.interactive
def test_xt_scaling(xt_scaling_pairs, data):
    for pair in xt_scaling_pairs:
        with open_loggs() as loggs:
            steps = [(l, xt(pair["edges"])) for l in pair["energies"]]
            links = [data[l] for l in pair["energies"]]
            ComparePipeline(steps, plot=True).transform(links, loggs)
