import ROOT
import json
import pytest  # noqa
import numpy as np
import pandas as pd
import uncertainties.unumpy as unp

import spectrum.broot as br
from spectrum.spectra import spectrum
from spectrum.plotter import plot
from spectrum.constants import invariant_cross_section_code


@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle, ranges", [
    ("#pi^{0}", [0.8, 20]),
    ("#eta", [2.0, 20]),
])
def test_tsallis_tcm_fit(particle, ranges, tsallis, ltitle, stop, oname):
    cs = spectrum(particle)
    tsallis.SetName("TsallisFullRange")
    tsallis.SetRange(*ranges)
    cs.Fit(tsallis, "QR")
    br.report(tsallis, particle)
    plot(
        [cs, tsallis],
        stop=stop,
        ytitle=invariant_cross_section_code(),
        xtitle="#it{p}_{T} (GeV/#it{c})",
        ltitle=ltitle,
        legend_pos=(0.65, 0.7, 0.8, 0.88),
        more_logs=False,
        oname=oname.format("phenomenology/tsallis_issues_"),
    )
    plot(
        [br.ratio(cs, tsallis)],
        stop=stop,
        logy=False,
        ytitle="#frac{Data}{Tsallis fit}",
        xtitle="#it{p}_{T} (GeV/#it{c})",
        legend_pos=None,
        more_logs=False,
        oname=oname.format("phenomenology/tsallis_issues_ratio_"),
    )


@pytest.fixture
def data():
    with open("config/predictions/tsallis.json") as f:
        data = json.load(f)
    return data


@pytest.fixture
def fy(target):
    if target == "n":
        return lambda x: 1 + 1 / (x - 1)
    return lambda x: x


@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("target, ytitle, ylimits", [
    ("n", "#it{q}", (1.1, 1.25)),
    ("C", "#it{T} (GeV)", (0.1, 0.3)),
])
def test_params(data, ytitle, ylimits, target, stop, coname):
    # print(pars)

    def data2graph(particle):
        pars = pd.DataFrame(data[particle].values())
        x = pars["energy"]
        y = unp.uarray(pars[target], pars["d{}".format(target)])
        if target == "n":
            y = 1 + 1 / (y - 1)
        graph = br.graph(
            "test",
            x,
            unp.nominal_values(y),
            np.zeros_like(x),
            unp.std_devs(y)
        )
        graph.SetMarkerColor(4)
        graph.SetMarkerStyle(21)
        graph.SetTitle(particle)
        return graph

    pion = data2graph("#pi^{0}")
    eta = data2graph("#eta")

    if target == "n":
        fitf = ROOT.TF1(
            "etaPionEnergyTsallisq",
            "[0] * TMath::Log(x[0]) + [1]",
            0.8, 1400)
        fitf.SetTitle("#it{a} log(#it{s}) + #it{b}")
        fitf.SetParNames(*["A", "B"])
        fitf.SetLineColor(ROOT.kBlack)
        fitf.SetLineWidth(2)
        fitf.SetParameter(0, 0)
        fitf.SetParameter(1, 0.11)

        multigraph = ROOT.TMultiGraph()
        multigraph.Add(pion)
        multigraph.Add(eta)
        multigraph.Fit(fitf)
        br.report(fitf)
        plots = [pion, eta, fitf]

    if target == "C":
        title = "#it{{T}}_{{{title}}} = {a:4.3f} #pm {b:4.3f}"
        fitf_pion = ROOT.TF1("pionEnergyTsallisT", "[0]", 0.8, 1400)
        fitf_pion.SetTitle("#it{a} log(#it{s}) + #it{b}")
        fitf_pion.SetParName(0, "T")
        fitf_pion.SetLineColor(ROOT.kRed + 1)
        fitf_pion.SetLineWidth(4)
        # fitf_pion.SetLineStyle(7)
        fitf_pion.SetParameter(0, 0)
        pion.Fit(fitf_pion, "0QN")
        br.report(fitf_pion)
        fitf_pion.SetTitle(
            title.format(
                title="#pi^{0}",
                a=fitf_pion.GetParameter(0),
                b=fitf_pion.GetParError(0),
            )
        )

        fitf_eta = ROOT.TF1("etaEnergyTsallisT", "[0]", 0.8, 1400)
        fitf_eta.SetTitle("#it{T}_{#eta}")
        fitf_eta.SetParName(0, "T")
        fitf_eta.SetLineColor(ROOT.kBlue + 1)
        fitf_eta.SetLineWidth(4)
        # fitf_eta.SetLineStyle(7)
        fitf_eta.SetParameter(0, 0)
        eta.Fit(fitf_eta, "0QN")
        br.report(fitf_eta)
        fitf_eta.SetTitle(
            title.format(
                title="#eta",
                a=fitf_eta.GetParameter(0),
                b=fitf_eta.GetParError(0)
            )
        )

        plots = [pion, eta, fitf_pion, fitf_eta]

    ROOT.gStyle.SetOptFit(0)
    plot(
        plots,
        stop=stop,
        logy=False,
        ytitle=ytitle,
        xtitle="#sqrt{#it{s}} (GeV)",
        ylimits=ylimits,
        xlimits=(0.7, 15),
        legend_pos=(0.6, 0.7, 0.75, 0.85),
        oname=coname.format("phenomenology/tsallis_parameter_"),
    )
