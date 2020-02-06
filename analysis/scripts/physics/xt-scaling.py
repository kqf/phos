import ROOT
import pytest
import json
import six
import numpy as np
import uncertainties as uc
import uncertainties.unumpy as unp
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

NOISY_COMBINATIONS = {(8000, 13000), (7000, 8000), (7000, 13000)}


class DataExtractor(TransformerBase):
    def transform(self, particle, loggs):
        hist = spectrum(particle)
        hist.energy = 13000
        hist.SetTitle("pp, #sqrt{#it{s}} = 13 TeV")
        return hist


class XTtransformer(TransformerBase):
    def transform(self, x, loggs):
        edges = br.edges(x.tot)
        xtedges = 2 * edges / x.energy

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
        x.Fit(fitf, "Q")
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
def n_factor(cs1, cs2_approx, s1, s2,):
    contents, errors, xT, _ = br.bins(cs1)
    spectrum1 = unp.uarray(contents, errors)
    pT = xT * s2 / 2
    spectrum2 = np.fromiter(map(cs2_approx.Eval, pT), np.float64)
    n = -unp.log(spectrum1 / spectrum2) / np.log(s1 / s2)
    nxt = cs1.Clone()
    for i, c in zip(br.hrange(nxt), n):
        nxt.SetBinContent(i, uc.nominal_value(c))
        nxt.SetBinError(i, uc.std_dev(c))
    return nxt


@n_factor.register(br.PhysicsHistogram, br.PhysicsHistogram)
def _(hist1, hist2):
    s1 = hist1.energy
    s2 = hist2.energy

    if (s1, s2) in NOISY_COMBINATIONS:
        return None

    results = br.PhysicsHistogram(
        n_factor(hist1.tot, hist2.fitf, s1, s2),
        n_factor(hist1.stat, hist2.fitf, s1, s2),
        n_factor(hist1.syst, hist2.fitf, s1, s2),
    )
    template = "#it{{n}} (#it{{x}}_{{T}}, {:.3g} TeV, {:.3g} TeV)"
    results.SetTitle(template.format(s1 / 1000., s2 / 1000))
    return results


@pytest.fixture
def xt_data(particle, tcm, xt_measured):
    with open("config/predictions/hepdata.json") as f:
        data = json.load(f)[particle]
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


@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta",
])
def test_plot_xt_distribution(xt_data, ltitle, oname):
    plot(
        xt_data[::-1],
        ytitle=invariant_cross_section_code(),
        xtitle="#it{x}_{T}",
        csize=(96, 128),
        ltitle=ltitle,
        legend_pos=(0.24, 0.15, 0.5, 0.35),
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
def test_calculate_combined_n(particle, n_factors, xtrange):
    multigraph = ROOT.TMultiGraph()
    for i, n in enumerate(n_factors):
        ngraph = br.hist2graph(n.tot)
        ngraph.SetMarkerColor(br.icolor(i))
        ngraph.SetLineColor(br.icolor(i))
        ngraph.SetMarkerStyle(20)
        ngraph.SetMarkerSize(1)
        multigraph.Add(ngraph)

    fitf = ROOT.TF1("xtCombined", "[0]", 1.e-04, 1.5e-02)
    fitf.SetParName(0, "n")

    fitf.SetLineWidth(3)
    fitf.SetParameter(0, 5.0)
    fitf.SetLineStyle(7)
    fitf.SetLineColor(ROOT.kBlack)
    multigraph.Fit(fitf, "RF", "", *xtrange)
    br.report(fitf)
    # plot(n_factors + [fitf], logy=False)
    return fitf.GetParameter(0), fitf.GetParError(0)


@pytest.fixture
def combined_n(n_factors, xtrange):
    return 5.04, 0.00919


@pytest.fixture
def xtrange():
    return 2.9e-03, 1.05e-02


@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle", ["#pi^{0}"])
@pytest.mark.parametrize("target", ["xt_scaling/n_factor_fit"])
def test_n_scaling_scaling(n_factors, xtrange, combined_n, coname):
    fitf = ROOT.TF1("nxt", "[0]", *xtrange)
    fitf.SetParameter(0, combined_n[0])
    fitf.SetLineColor(ROOT.kBlack)
    fitf.SetLineStyle(9)
    fitf.SetTitle("const = {:.3f} #pm {:.3f}".format(*combined_n))
    plot(
        [fitf] +
        n_factors,
        logx=False,
        logy=False,
        xlimits=(0.0001, 0.011),
        ylimits=(2, 8),
        ytitle="#it{n} (#it{x}_{T}, #sqrt{#it{s}_{1}}, #sqrt{#it{s}_{2}})",
        xtitle="#it{x}_{T}",
        csize=(96, 96 * 0.64),
        tmargin=0.01,
        rmargin=0.01,
        lmargin=0.1,
        yoffset=1.,
        legend_pos=(0.65, 0.65, 0.88, 0.95),
        oname=coname.format(""),
    )


# @pytest.mark.skip
@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta",
], scope="module")
def test_scaled_spectra(xt_data, combined_n, ltitle, oname):
    for h in xt_data:
        h.Scale(h.energy ** combined_n[0])
    title = "(#sqrt{{#it{{s}}}})^{{{n:.3f}}} (GeV)^{{{n:.3g}}} #times {t}"
    plot(
        xt_data[::-1],
        ytitle=title.format(n=combined_n[0], t=invariant_cross_section_code()),
        xtitle="#it{x}_{T}",
        ltitle=ltitle,
        more_logs=False,
        legend_pos=(0.24, 0.15, 0.5, 0.35),
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
