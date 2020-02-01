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


@pytest.mark.skip
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
        # xlimits=(0.7, 22),
        csize=(96, 128),
        ltitle=ltitle,
        legend_pos=(0.65, 0.7, 0.8, 0.88),
        yoffset=1.4,
        more_logs=False,
        oname=oname.format("phenomenology/tsallis_issues_"),
    )
    plot(
        [br.ratio(cs, tsallis)],
        stop=stop,
        logy=False,
        ytitle="#frac{Data}{Tsallis fit}",
        xtitle="#it{p}_{T} (GeV/#it{c})",
        csize=(96, 128),
        legend_pos=None,
        yoffset=1.4,
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

    fitf = ROOT.TF1("qEnergyDep", "[0] * TMath::Log(x[0]) + [1]", 0.8, 1400)
    fitf.SetTitle("#it{a} log(#it{s}) + #it{b}")
    fitf.SetParNames(*["a", "b"])
    fitf.SetLineColor(ROOT.kBlack)
    fitf.SetLineWidth(2)
    fitf.SetParameter(0, 0)
    fitf.SetParameter(1, 0.138)

    pion = data2graph("#pi^{0}")
    eta = data2graph("#eta")

    multigraph = ROOT.TMultiGraph()
    multigraph.Add(pion)
    multigraph.Add(eta)
    multigraph.Fit(fitf)

    br.report(fitf)
    plot(
        [pion, eta, fitf],
        stop=stop,
        logy=False,
        ytitle=ytitle,
        xtitle="#sqrt{#it{s}} (GeV)",
        ylimits=ylimits,
        xlimits=(0.7, 15),
        csize=(96, 128),
        legend_pos=(0.7, 0.7, 0.85, 0.80),
        yoffset=1.4,
        oname=coname.format("phenomenology/tsallis_parameter_"),
    )
