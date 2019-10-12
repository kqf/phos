import ROOT
import pytest
import json
import six
import numpy as np
import itertools

import spectrum.broot as br
import spectrum.sutils as su

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
        hist.logx = True
        hist.logy = True
        hist.label = item["title"]
        hist.Scale(item["scale"])
        hist.energy = item["energy"]
        hist.title = item["title"]
        return hist


class XTtransformer(TransformerBase):
    def transform(self, x, loggs):
        edges = np.array([x.GetBinLowEdge(i)
                          for i in br.hrange(x, edges=True)])
        xtedges = edges / (x.energy / 2)
        xt = ROOT.TH1F(
            "{}_xt".format(x.GetName()), x.GetTitle(),
            len(xtedges) - 1,
            xtedges)

        for i in br.hrange(x):
            xt.SetBinContent(i, x.GetBinContent(i))
            xt.SetBinError(i, x.GetBinError(i) / 2)

        xt.logx = True
        xt.logy = True
        xt.label = str(x.energy)
        xt.energy = x.energy
        xt.fitfunc = x.fitfunc
        return xt


class DataFitter(TransformerBase):
    def __init__(self):
        with open("config/predictions/tsallis-pion.json") as f:
            self.data = json.load(f)

    def transform(self, x, loggs):
        tsallis = FVault().tf1("tsallis", x.title.replace("pp", "#pi^{0}"))
        x.fitfunc = tsallis
        return x


def xt(edges=None):
    return Pipeline([
        ("cyield", HepdataInput()),
        ("fit", DataFitter()),
        ("xt", XTtransformer()),
    ])


def n_factor(hist1, hist2):
    nxt = hist1.Clone("n")
    nxt2 = br.function2histogram(hist2.fitfunc, nxt, hist2.energy / 2)
    nxt.Divide(nxt2)
    contents, errors, centers = br.bins(nxt)
    logcontents = - np.log(contents)
    logerrors = errors / contents
    for (i, c, e) in zip(br.hrange(nxt), logcontents, logerrors):
        nxt.SetBinContent(i, c)
        nxt.SetBinError(i, e)
    nxt.Scale(1. / np.log(hist1.energy / hist2.energy))
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


@pytest.mark.skip("")
@pytest.mark.onlylocal
@pytest.mark.interactive
def test_xt_scaling(data):
    spectra = sorted(data, key=lambda x: x.energy)
    n_factors = [n_factor(*pair)
                 for pair in itertools.combinations(spectra, 2)]
    Comparator().compare(n_factors)


@pytest.mark.skip("")
@pytest.mark.onlylocal
@pytest.mark.interactive
def test_separate_fits(data):
    spectra = sorted(data, key=lambda x: x.energy)
    n_factors = [n_factor(*pair)
                 for pair in itertools.combinations(spectra, 2)]

    for n in n_factors:
        fit = ROOT.TF1("fitpol0", "[0]", 1.e-03, 5.e-02)
        fit.SetLineWidth(3)
        fit.SetParameter(0, 5.0)
        fit.SetLineStyle(7)
        fit.SetLineColor(ROOT.kBlack)
        n.Fit("fitpol0", "FQ", "", 2.9e-03, 2.e-02)  # 19/07/2017
        Comparator().compare(n)

    # mg->Fit("fitpol0","FQ","",4.4e-03,2.e-02);
    # mg->Fit("fitpol0","FQ","",1.0e-03,2.e-02);## 2/10/2017
    # print("\n pi0 Combined Fit \n")
    # print("#chi^{2}/ndf = %.3g \n", fit.GetChisquare() / fit.GetNDF())
    # print("n = %.3g +- %.3g \n", fit.GetParameter(0), fit.GetParError(0))


@pytest.mark.onlylocal
@pytest.mark.interactive
def test_combined_fits(data):
    spectra = sorted(data, key=lambda x: x.energy)
    n_factors = [n_factor(*pair)
                 for pair in itertools.combinations(spectra, 2)]

    multigraph = ROOT.TMultiGraph()
    for i, n in enumerate(n_factors):
        ngraph = br.hist2graph(n)
        ngraph.SetMarkerColor(br.icolor(i))
        ngraph.SetLineColor(br.icolor(i))
        ngraph.SetMarkerStyle(20)
        ngraph.SetMarkerSize(1)
        multigraph.Add(ngraph)

    fitf = ROOT.TF1("fitpol0", "[0]", 1.e-03, 5.e-02)
    fitf.SetLineWidth(3)
    fitf.SetParameter(0, 5.0)
    fitf.SetLineStyle(7)
    fitf.SetLineColor(ROOT.kBlack)
    multigraph.Fit(fitf, "FQ", "", 2.9e-03, 2.e-02)

    with su.canvas():
        multigraph.Draw("ap")
