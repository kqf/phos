import json
import pytest
import numpy as np
import pandas as pd
import ROOT

import uncertainties.unumpy as unp
import spectrum.broot as br
from spectrum.plotter import plot

from spectrum.spectra import energies, DataEnergiesExtractor
from spectrum.pipeline import FunctionTransformer
from spectrum.pipeline import DataFitter, Pipeline


def fitted(fitf, ptmax=15):
    def p(x, loggs):
        res = br.fit_results(x.fitf)
        print(res["Te"], res["T"], res["T"] / res["Te"], x.energy)
        br.report(x.fitf, limits=True)
        return x

    def fit_results(x, loggs):
        res = br.fit_results(x.fitf)
        res["energy"] = x.energy / 1000
        return res

    return Pipeline([
        ("cyield", DataEnergiesExtractor()),
        ("fit", DataFitter(fitf, xmax=ptmax)),
        ("show", FunctionTransformer(p)),
        ("res", FunctionTransformer(fit_results)),
    ])


@pytest.fixture
def rawdata(particle, tcm):
    return energies(particle, fitted(tcm))


# @pytest.mark.skip
@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta",
])
def test_updates_parameters(particle, rawdata, ltitle):
    with open("config/predictions/tcm.json") as f:
        final = json.load(f)
    final[particle] = rawdata
    with open("config/predictions/tcm.json", "w") as f:
        json.dump(final, f, indent=4)


@pytest.fixture
def data():
    with open("config/predictions/tcm.json") as f:
        data = json.load(f)
    return data


@pytest.fixture
def charge_particles_t2():
    df = pd.read_csv("config/predictions/tcm-t2-te2-charged.csv")
    graph = br.graph(
        "charged",
        df["Te2"],
        df["T2"],
        dy=df["upper errors"] - df["lower errors"],
    )
    graph.SetMarkerStyle(21)
    graph.SetTitle("Charged particles")
    return graph


@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("target", ["r"])
def test_r(data, stop, coname):
    # print(pars)

    def data2graph(particle):
        pars = pd.DataFrame(data[particle])
        A = unp.uarray(pars["A"], pars["dA"])
        n = unp.uarray(pars["n"], pars["dn"])
        Te = unp.uarray(pars["Te"], pars["dTe"])
        T = unp.uarray(pars["T"], pars["dT"])
        Ae = unp.uarray(pars["Ae"], pars["dAe"])
        M = pars["M"]

        r = A * n * T / (
            A * n * T + Ae * (2 * M * Te + 2 * Te ** 2) * (n - 1)
        )
        y = unp.nominal_values(r)
        dy = unp.std_devs(r)
        x = pars["energy"]
        graph = br.graph("test", x, y, np.zeros_like(x), dy)
        graph.SetMarkerStyle(21)
        graph.SetTitle(particle)

        fitf = ROOT.TF1("{}R_tcm".format(br.spell(particle)), "[0]", 0.8, 1400)
        fitf.SetParName(0, "T")
        fitf.SetLineColor(ROOT.kRed + 1)
        fitf.SetLineWidth(2)
        # fitf.SetLineStyle(7)
        fitf.SetParameter(0, 0)
        graph.Fit(fitf, "0QN")
        fitf.SetTitle("#it{{R }}_{{TCM}}^{{{}}}= {:4.3f} #pm {:4.3f}".format(
            particle,
            fitf.GetParameter(0),
            fitf.GetParError(0)
        ))
        br.report(fitf)
        return graph, fitf

    pion, pionf = data2graph("#pi^{0}")
    eta, etaf = data2graph("#eta")
    pionf.SetLineColor(ROOT.kRed + 1)
    etaf.SetLineColor(ROOT.kBlue + 1)
    plot(
        [pion, eta, pionf, etaf],
        stop=stop,
        logy=False,
        ytitle="#it{R}_{_{TCM}}",
        xtitle="#sqrt{#it{s}} (GeV)",
        ylimits=(0.01, 2.6),
        xlimits=(0.7, 15),
        csize=(96, 128),
        legend_pos=(0.55, 0.7, 0.75, 0.85),
        oname=coname.format("phenomenology/tcm_parameter_"),
    )


@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("target", ["corr"])
def test_corr(data, charge_particles_t2, stop, coname):
    # print(pars)

    def data2graph(particle):
        pars = pd.DataFrame(data[particle])
        ux = unp.uarray(pars["Te"], pars["dTe"]) ** 2
        uy = unp.uarray(pars["T"], pars["dT"]) ** 2
        # print(particle)
        # print(unp.nominal_values(ux))
        pars["Te2"] = unp.nominal_values(ux)
        pars["T2"] = unp.nominal_values(uy)
        pars["dTe2"] = unp.std_devs(ux)
        pars["dT2"] = unp.std_devs(uy)
        print()
        # print(pars[["energy", "Te2", "dTe2", "T2", "dT2"]])
        # print(pars[["energy", "Te", "dTe", "T", "dT"]])
        graph = br.graph(
            "test",
            pars["Te2"],
            pars["T2"],
            pars["dTe2"],
            pars["dT2"],
        )
        graph.SetMarkerStyle(21)
        graph.SetTitle(particle)
        return graph

    # func = ROOT.TF1("f", "17.5 * x[0]", 0, 1)
    plot(
        [
            data2graph("#pi^{0}"),
            data2graph("#eta"),
            charge_particles_t2,
            # func,
        ],
        stop=stop,
        logy=False,
        logx=False,
        ytitle="#it{T}^{ 2} (GeV^{2})",
        xtitle="#it{T}_{#it{e}}^{ 2} (GeV^{2})",
        # ylimits=(0.01, 2.6),
        # xlimits=(0., 0.1),
        # csize=(96, 128),
        legend_pos=(0.65, 0.7, 0.8, 0.80),
        options="qp",
        oname=coname.format("phenomenology/tcm_parameter_"),
    )


@pytest.mark.skip
def test_charged_particles(charge_particles_t2):
    plot(
        [charge_particles_t2],
        logy=False,
        logx=False,
        xlimits=(0., 0.04),
        ylimits=(0., 0.8),
        legend_pos=None,
    )
