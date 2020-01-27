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
        ytitle="R_{TCM}(s)",
        xtitle="#sqrt{#it{s}} (GeV)",
        ylimits=(0.01, 2.6),
        xlimits=(0.7, 15),
        csize=(96, 128),
        legend_pos=(0.75, 0.7, 0.9, 0.80),
        yoffset=1.4,
        oname=coname.format("phenomenology/tcm_parameter_"),
    )


@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("target", ["corr"])
def test_corr(data, stop, coname):
    # print(pars)

    def data2graph(particle):
        pars = pd.DataFrame(data[particle].values())
        ux = unp.uarray(pars["Te"], pars["dTe"]) ** 2
        uy = unp.uarray(pars["T"], pars["dT"]) ** 2
        graph = br.graph(
            "test",
            unp.nominal_values(ux),
            unp.nominal_values(uy),
            unp.std_devs(ux),
            unp.std_devs(uy),
        )
        graph.SetMarkerStyle(21)
        graph.SetTitle(particle)
        return graph

    plot(
        [data2graph("#pi^{0}"), data2graph("#eta")],
        stop=stop,
        logy=False,
        logx=False,
        ytitle="T^{2} (GeV^{2})",
        xtitle="T_{e}^{2} (GeV^{2})",
        # ylimits=(0.01, 2.6),
        # xlimits=(0.7, 15),
        csize=(96, 128),
        legend_pos=(0.75, 0.7, 0.9, 0.80),
        yoffset=1.4,
        options="qp",
        oname=coname.format("phenomenology/tcm_parameter_"),
    )
