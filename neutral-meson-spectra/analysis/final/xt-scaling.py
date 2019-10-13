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
    spectra = sorted(histograms, key=lambda x: x.energy)
    return spectra


@pytest.mark.skip("")
@pytest.mark.onlylocal
@pytest.mark.interactive
def test_xt_distribution(data):
    Comparator().compare(data)


@pytest.mark.skip("")
@pytest.mark.onlylocal
@pytest.mark.interactive
def test_n_scaling_scaling(data):
    spectra = sorted(data, key=lambda x: x.energy)
    n_factors = [n_factor(*pair)
                 for pair in itertools.combinations(spectra, 2)]
    Comparator().compare(n_factors)


@pytest.fixture
def xtrange():
    return 2.9e-03, 2.e-02


@pytest.mark.skip("")
@pytest.mark.onlylocal
@pytest.mark.interactive
def test_separate_fits(data, xtrange):
    spectra = sorted(data, key=lambda x: x.energy)
    n_factors = [n_factor(*pair)
                 for pair in itertools.combinations(spectra, 2)]

    for n in n_factors:
        fitf = ROOT.TF1("fitpol0", "[0]", 1.e-03, 5.e-02)
        fitf.SetLineWidth(3)
        fitf.SetParameter(0, 5.0)
        fitf.SetLineStyle(7)
        fitf.SetLineColor(ROOT.kBlack)
        n.Fit(fitf, "FQ", "", *xtrange)
        br.print_fit_results(fitf)
        Comparator().compare(n)


@pytest.mark.skip("")
@pytest.mark.onlylocal
@pytest.mark.interactive
def test_combined_fits(data, xtrange):
    n_factors = [n_factor(*pair)
                 for pair in itertools.combinations(data, 2)]

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
    multigraph.Fit(fitf, "FQ", "", *xtrange)
    br.print_fit_results(fitf)

    with su.canvas():
        multigraph.Draw("ap")


@pytest.fixture
def combined_n():
    return 5.19


@pytest.mark.skip("")
@pytest.mark.onlylocal
@pytest.mark.interactive
def test_scaled_spectra(data, combined_n):
    for h in data:
        h.Scale(h.energy ** combined_n)
    Comparator().compare(data)


@pytest.fixture
def scaledf():
    func = FVault().tf1("tcm", "xT")
    func.FixParameter(5, func.GetParameter(5))
    return func


@pytest.mark.onlylocal
@pytest.mark.interactive
def test_xt_scaling(data, combined_n, scaledf):
    for h in data:
        h.Scale(h.energy ** combined_n)
        if h.energy < 1000:
            scaledf.SetParameter(0, 4.35967e+22)
            scaledf.SetParameter(1, 3.59107e-07)
            scaledf.SetParameter(2, 2.32103e+22)
            scaledf.SetParameter(3, -3.89363e-04)

        h.Fit(scaledf, "", "", 9e-05, 3.e-02)
        Comparator().compare(h)
        h.Divide(scaledf)
    Comparator().compare(data)

# 1  Ae           4.35967e+22   8.92836e+22   2.07885e+16  -8.53195e-27
# 2  Te           3.59240e-07   5.00738e-07   8.28673e-11  -3.88209e+02
# 3  A            2.32103e+22   4.19204e+22   1.10675e+16   3.65758e-26
# 4  T           -3.89363e-04   1.54462e-04   5.49227e-09  -1.39198e+01
# 5  n            3.11357e+00   2.46071e-01   3.93579e-05  -3.05920e-03
# 6  M            1.34976e-01     fixed
