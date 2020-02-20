import json
import pytest
import numpy as np
import pandas as pd

import uncertainties.unumpy as unp
import spectrum.broot as br
from spectrum.plotter import plot


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
        pars = pd.DataFrame(data[particle].values())
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
        return graph

    plot(
        [data2graph("#pi^{0}"), data2graph("#eta")],
        stop=stop,
        logy=False,
        ytitle="#it{R}_{_{TCM}}",
        xtitle="#sqrt{#it{s}} (GeV)",
        ylimits=(0.01, 2.6),
        xlimits=(0.7, 15),
        csize=(96, 128),
        legend_pos=(0.75, 0.7, 0.9, 0.80),
        oname=coname.format("phenomenology/tcm_parameter_"),
    )


@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("target", ["corr"])
def test_corr(data, charge_particles_t2, stop, coname):
    # print(pars)

    def data2graph(particle):
        pars = pd.DataFrame(data[particle].values())
        ux = unp.uarray(pars["Te"], pars["dTe"]) ** 2
        uy = unp.uarray(pars["T"], pars["dT"]) ** 2
        # print(particle)
        # print(unp.nominal_values(ux))
        pars["Te2"] = unp.nominal_values(ux)
        pars["T2"] = unp.nominal_values(uy)
        pars["dTe2"] = unp.std_devs(ux)
        pars["dT2"] = unp.std_devs(uy)
        print()
        print(pars[["energy", "Te2", "dTe2", "T2", "dT2"]])
        print(pars[["energy", "Te", "dTe", "T", "dT"]])
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
        ylimits=(0.01, 2.6),
        xlimits=(0., 0.1),
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
