import ROOT
import pytest
import json
import six
import numpy as np
import itertools

import spectrum.broot as br
from multimethod import multimethod

from spectrum.pipeline import TransformerBase, Pipeline
from spectrum.pipeline import ParallelPipeline, FunctionTransformer
from spectrum.comparator import Comparator
from spectrum.output import open_loggs
from spectrum.spectra import spectrum
from spectrum.plotter import plot
from spectrum.constants import invariant_cross_section_code
from spectrum.vault import FVault

DATA_CONFIG = {
    "#pi^{0}": "config/predictions/hepdata-pion.json",
    "#eta": "config/predictions/hepdata-eta.json",
}


class DataExtractor(TransformerBase):
    def transform(self, particle, loggs):
        hist = spectrum(particle)
        hist.energy = 13000
        hist.SetTitle("pp, #sqrt{#it{s}} = 13 TeV")
        return hist


class XTtransformer(TransformerBase):
    def transform(self, x, loggs):
        edges = br.edges(x.tot)
        xtedges = edges / (x.energy / 2)

        xt = br.PhysicsHistogram(
            self._transform(x.tot, xtedges),
            self._transform(x.stat, xtedges),
            self._transform(x.syst, xtedges),
        )
        xt.energy = x.energy
        xt.fitf = x.fitf
        return xt

    @staticmethod
    def _transform(hist, edges):
        return br.table2hist(
            "{}_xt".format(hist.GetName()),
            hist.GetTitle(),
            br.bins(hist).contents,
            br.bins(hist).errors,
            edges
        )


class DataFitter(TransformerBase):
    def __init__(self, fitf):
        self.fitf = fitf

    def transform(self, x, loggs):
        fitf = self.fitf.Clone()
        x.Fit(fitf)
        x.fitf = fitf
        return x


def xt(fitf):
    return Pipeline([
        ("cyield", FunctionTransformer(br.from_hepdata, True)),
        ("fit", DataFitter(fitf)),
        ("xt", XTtransformer()),
    ])


@pytest.fixture
def xt_measured(particle, tcm):
    estimator = Pipeline([
        ("cyield", DataExtractor()),
        ("fit", DataFitter(tcm)),
        ("xt", XTtransformer())
    ])
    with open_loggs() as loggs:
        result = estimator.transform(particle, loggs)
    return result


@multimethod
def n_factor(hist1, hist2, s1, s2, func):
    nxt = hist1.Clone()
    nxt2 = br.function2histogram(func, nxt, s2 / 2)
    nxt.Divide(nxt2)
    contents, errors, centers = br.bins(nxt)
    logcontents = - np.log(contents)
    logerrors = 4 * errors / contents
    for (i, c, e) in zip(br.hrange(nxt), logcontents, logerrors):
        nxt.SetBinContent(i, c)
        nxt.SetBinError(i, e)
    nxt.Scale(1. / np.log(s1 / s2))
    # nxt.label = "n(x_{{T}}, {}, {})".format(hist1.label, hist2.label)
    # nxt.SetTitle(nxt.label.replace("pp", ""))
    return nxt


@n_factor.register(br.PhysicsHistogram, br.PhysicsHistogram)
def _(hist1, hist2):
    ignore = {(8000, 13000), (7000, 8000), (7000, 13000)}
    s1 = hist1.energy
    s2 = hist2.energy

    if (s1, s2) in ignore:
        return None

    results = br.PhysicsHistogram(
        n_factor(hist1.tot, hist2.tot, s1, s2, hist2.fitf),
        n_factor(hist1.stat, hist2.stat, s1, s2, hist2.fitf),
        n_factor(hist1.syst, hist2.syst, s1, s2, hist2.fitf),
    )
    template = "#it{{n}} (#it{{x}}_{{T}}, {:.3g} TeV, {:.3g} TeV)"
    results.SetTitle(template.format(s1 / 1000., s2 / 1000))
    return results


@pytest.fixture
def xt_data(particle, tcm, xt_measured):
    with open(DATA_CONFIG[particle]) as f:
        data = json.load(f)
    labels, links = zip(*six.iteritems(data))
    with open_loggs() as loggs:
        steps = [(l, xt(tcm)) for l in labels]
        histograms = ParallelPipeline(steps).transform(links, loggs)
    spectra = sorted(histograms, key=lambda x: x.energy)
    spectra.append(xt_measured)
    return spectra


@pytest.fixture
def n_factors(xt_data):
    spectra = sorted(xt_data, key=lambda x: x.energy)
    n_factors = [n_factor(*pair)
                 for pair in itertools.combinations(spectra, 2)]
    n_factors = [n for n in n_factors if n is not None]
    return n_factors


@pytest.mark.skip
@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta",
])
def test_plot_xt_distribution(xt_data, particle, ltitle, oname):
    plot(
        xt_data,
        ytitle=invariant_cross_section_code(),
        csize=(96, 128),
        ltitle=ltitle,
        legend_pos=(0.72, 0.7, 0.88, 0.88),
        yoffset=1.4,
        more_logs=False,
        oname=oname.format("xt_scaling/xt_cross_section_"),
    )


@pytest.mark.skip("just for debug purposes")
@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle", ["#pi^{0}"])
def test_separate_fits(n_factors, xtrange):
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
def test_combined_fits(n_factors, xtrange):
    multigraph = ROOT.TMultiGraph()
    for i, n in enumerate(n_factors):
        ngraph = br.hist2graph(n.tot)
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
def test_n_scaling_scaling(n_factors, xtrange, combined_n):
    fitf = ROOT.TF1("nxt", "[0]", *xtrange)
    fitf.SetParameter(0, combined_n)
    fitf.SetLineColor(ROOT.kBlack)
    fitf.SetLineStyle(9)
    fitf.SetTitle("const = {}".format(combined_n))
    plot(
        [fitf] +
        n_factors,
        logx=False,
        logy=False,
        xlimits=(0.0001, 0.011),
        ylimits=(0, 12),
        ytitle="#it{n} (#it{x}_{T}, #sqrt{#it{s}_{1}}, #sqrt{#it{s}_{2}})",
        xtitle="x_{T}",
        csize=(96 * 1.5, 96),
        legend_pos=(0.65, 0.6, 0.88, 0.88),
        oname="results/discussion/xt_scaling/n_factor_fit.pdf",
    )


@pytest.mark.skip
@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta",
])
def test_scaled_spectra(particle, xt_data, combined_n, ltitle, oname):
    for h in xt_data:
        h.Scale(h.energy ** combined_n)
    template = "(#sqrt{{#it{{s}}}})^{{{n}}} (GeV)^{{{n}}} #times "
    title = template.format(n=combined_n)
    title += invariant_cross_section_code().strip()
    plot(
        xt_data,
        ytitle=title,
        ylimits=(0.1e16, 0.5e26),
        xlimits=(1e-4, 0.013),
        csize=(96, 128),
        ltitle=ltitle,
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


@pytest.mark.skip
@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta",
])
def test_xt_scaling(particle, xt_data, combined_n, scaledf):
    for h in xt_data:
        h.Scale(h.energy ** combined_n)
        if h.energy == 8000:
            scaledf.SetParameter(0, 2e22)
            scaledf.SetParameter(2, 2e22)
            h.Fit(scaledf, "", "", 9e-05, 3.e-02)
        Comparator().compare(h)
    for h in xt_data:
        h.Divide(scaledf)
    plot(xt_data)
