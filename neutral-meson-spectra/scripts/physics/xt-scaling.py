import ROOT
import pytest
import json
import six
import numpy as np
import itertools

import spectrum.broot as br

from spectrum.pipeline import TransformerBase, Pipeline
from spectrum.pipeline import ParallelPipeline
from spectrum.comparator import Comparator
from spectrum.output import open_loggs
from spectrum.spectra import spectrum
from spectrum.plotter import plot
from spectrum.constants import invariant_cross_section_code
from vault.formulas import FVault

DATA_CONFIG = {
    "#pi^{0}": "config/predictions/hepdata-pion.json",
    "#eta": "config/predictions/hepdata-eta.json",
}


class HepdataInput(TransformerBase):
    def __init__(self, table_name="Table 1",
                 histname="Graph1D_y1", plot=False):
        super(HepdataInput, self).__init__(plot)
        self.histname = histname

    def transform(self, item, loggs):
        filename = ".hepdata-cachedir/{}".format(item["file"])
        br.io.hepdata(item["hepdata"], filename, item["table"])
        graph = br.io.read(filename, item["table"], self.histname)
        hist = br.graph2hist(graph)
        hist = br.scale_clone(hist, item["scale"])
        hist.logx = True
        hist.logy = True
        hist.label = item["title"]
        hist.func = item["func"]
        hist.energy = item["energy"]
        hist.title = item["title"]
        hist.SetTitle(item["title"])
        return hist


class DataExtractor(TransformerBase):
    def transform(self, particle, loggs):
        hist = spectrum(particle)
        for i in br.hrange(hist):
            hist.SetBinContent(i, hist.GetBinContent(i))
        hist.logx = True
        hist.logy = True
        hist.label = "13 TeV"
        hist.energy = 13000
        hist.title = "pp 13 TeV"
        hist.func = "#pi^{0} 13 TeV"
        hist.SetTitle("pp 13 TeV")
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
        xt.GetXaxis().SetTitle("x_{T}")

        for i in br.hrange(x):
            xt.SetBinContent(i, x.GetBinContent(i))
            xt.SetBinError(i, x.GetBinError(i))

        xt.logx = True
        xt.logy = True
        xt.label = x.label
        xt.energy = x.energy
        xt.fitfunc = x.fitfunc
        return xt


class DataFitter(TransformerBase):
    def __init__(self):
        with open("config/predictions/tsallis-pion.json") as f:
            self.data = json.load(f)

    def transform(self, x, loggs):
        tsallis = FVault().tf1("tsallis", x.func)
        x.fitfunc = tsallis
        return x


def xt(edges=None):
    return Pipeline([
        ("cyield", HepdataInput()),
        ("fit", DataFitter()),
        ("xt", XTtransformer()),
    ])


def xt_measured(particle):
    estimator = Pipeline([
        ("cyield", DataExtractor()),
        ("fit", DataFitter()),
        ("xt", XTtransformer())
    ])
    with open_loggs() as loggs:
        result = estimator.transform(particle, loggs)
    return result


def n_factor(hist1, hist2):
    ignore = {(8000, 13000), (7000, 8000), (7000, 13000)}
    if (hist1.energy, hist2.energy) in ignore:
        return None
    nxt = hist1.Clone()
    nxt2 = br.function2histogram(hist2.fitfunc, nxt, hist2.energy / 2)
    nxt.Divide(nxt2)
    contents, errors, centers = br.bins(nxt)
    logcontents = - np.log(contents)
    logerrors = 4 * errors / contents
    for (i, c, e) in zip(br.hrange(nxt), logcontents, logerrors):
        nxt.SetBinContent(i, c)
        nxt.SetBinError(i, e)
    nxt.Scale(1. / np.log(hist1.energy / hist2.energy))
    nxt.label = "n(x_{{T}}, {}, {})".format(hist1.label, hist2.label)
    nxt.SetTitle(nxt.label.replace("pp", ""))
    return nxt


@pytest.fixture
def data(particle):
    with open(DATA_CONFIG[particle]) as f:
        data = json.load(f)
    labels, links = zip(*six.iteritems(data))
    steps = [(l, xt()) for l in labels]
    with open_loggs() as loggs:
        histograms = ParallelPipeline(steps).transform(links, loggs)
    spectra = sorted(histograms, key=lambda x: x.energy)
    spectra.append(xt_measured(particle))
    return spectra


@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta",
])
def test_plot_xt_distribution(data, particle, oname):
    plot(
        data,
        ytitle=invariant_cross_section_code(),
        csize=(96, 128),
        ltitle="{} #rightarrow #gamma#gamma".format(particle),
        legend_pos=(0.72, 0.7, 0.88, 0.88),
        yoffset=1.4,
        more_logs=False,
        oname=oname.format("xt_scaling/xt_cross_section_"),
    )


@pytest.mark.skip("just for debug purposes")
@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle", ["#pi^{0}"])
def test_separate_fits(data, xtrange):
    spectra = sorted(data, key=lambda x: x.energy)
    n_factors = [n_factor(*pair)
                 for pair in itertools.combinations(spectra, 2)]
    n_factors = [n for n in n_factors if n is not None]

    for n in n_factors:
        fitf = ROOT.TF1("fitpol0", "[0]", 1.e-03, 5.e-02)
        fitf.SetLineWidth(3)
        fitf.SetParameter(0, 5.0)
        fitf.SetLineStyle(7)
        fitf.SetLineColor(ROOT.kBlack)
        n.Fit(fitf, "FQ", "", *xtrange)
        # br.print_fit_results(fitf)
        plot([n, fitf], logy=False)


@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle", ["#pi^{0}"])
def test_combined_fits(data, xtrange):
    n_factors = [n_factor(*pair)
                 for pair in itertools.combinations(data, 2)]
    n_factors = [n for n in n_factors if n is not None]

    multigraph = ROOT.TMultiGraph()
    for i, n in enumerate(n_factors):
        ngraph = br.hist2graph(n)
        ngraph.SetMarkerColor(br.icolor(i))
        ngraph.SetLineColor(br.icolor(i))
        ngraph.SetMarkerStyle(20)
        ngraph.SetMarkerSize(1)
        multigraph.Add(ngraph)

    fitf = ROOT.TF1("fitpol0", "[0]", 1.e-03, 1.5e-02)
    fitf.SetLineWidth(3)
    fitf.SetParameter(0, 5.0)
    fitf.SetLineStyle(7)
    fitf.SetLineColor(ROOT.kBlack)
    multigraph.Fit(fitf, "RF", "", *xtrange)
    br.print_fit_results(fitf)
    plot(n_factors + [fitf], logy=False)


@pytest.fixture
def xtrange():
    return 2.9e-03, 1.05e-02


@pytest.fixture
def combined_n():
    # chi^{2}/ndf = 1.868
    # p0 = 5.302
    # Delta p0 = 0.044
    return 5.302


@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle", ["#pi^{0}"])
def test_n_scaling_scaling(data, xtrange, combined_n):
    spectra = sorted(data, key=lambda x: x.energy)
    n_factors = [n_factor(*pair)
                 for pair in itertools.combinations(spectra, 2)]
    n_factors = [n for n in n_factors if n is not None]
    fitfunc = ROOT.TF1("nxt", "[0]", *xtrange)
    fitfunc.SetParameter(0, combined_n)
    fitfunc.SetLineColor(ROOT.kBlack)
    fitfunc.SetLineStyle(9)
    fitfunc.SetTitle("const = {}".format(combined_n))
    plot(
        [fitfunc] +
        n_factors,
        logx=False,
        logy=False,
        xlimits=(0.0001, 0.011),
        ylimits=(0, 12),
        ytitle="n(x_{T}, #sqrt{s_{1}}, #sqrt{s_{2}})",
        xtitle="x_{T}",
        csize=(96 * 1.5, 96),
        legend_pos=(0.65, 0.6, 0.88, 0.88),
        oname="results/discussion/xt_scaling/n_factor_fit.pdf",
    )


@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta",
])
def test_scaled_spectra(particle, data, oname, combined_n):
    for h in data:
        h.Scale(h.energy ** combined_n)
    title = "(#sqrt{{s}})^{{{n}}} (GeV)^{{{n}}} #times ".format(n=combined_n)
    title += invariant_cross_section_code().strip()
    plot(
        data,
        ytitle=title,
        ylimits=(0.1e16, 0.5e26),
        xlimits=(1e-4, 0.013),
        csize=(96, 128),
        ltitle="{} #rightarrow #gamma#gamma".format(particle),
        legend_pos=(0.72, 0.7, 0.88, 0.88),
        yoffset=1.7,
        more_logs=False,
        oname=oname.format("xt_scaling/xt_normalized_cross_section_"),
    )


@pytest.fixture
def scaledf():
    func = FVault().tf1("tcm", "xT")
    func.FixParameter(5, func.GetParameter(5))
    return func


@pytest.mark.skip("")
@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta",
])
def test_xt_scaling(particle, data, combined_n, scaledf):
    for h in data:
        h.Scale(h.energy ** combined_n)
        if h.energy == 8000:
            scaledf.SetParameter(0, 2e22)
            scaledf.SetParameter(2, 2e22)
            h.Fit(scaledf, "", "", 9e-05, 3.e-02)
        Comparator().compare(h)
    for h in data:
        h.Divide(scaledf)
    plot(data)
