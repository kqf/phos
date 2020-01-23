import json
import pytest  # noqa
import numpy as np
import pandas as pd

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
    # ("#eta", [2.0, 20]),
])
def test_tsallis_tcm_fit(particle, ranges, tsallis, ltitle, stop, oname):
    cs = spectrum(particle)
    tsallis.SetRange(*ranges)
    cs.Fit(tsallis, "QR")
    br.report(tsallis, particle)
    plot(
        [cs, tsallis],
        ytitle=invariant_cross_section_code(),
        xtitle="p_{T} (GeV/#it{c})",
        # xlimits=(0.7, 22),
        csize=(96, 128),
        ltitle=ltitle,
        legend_pos=(0.65, 0.7, 0.8, 0.88),
        yoffset=1.4,
        more_logs=False,
        oname=oname.format("phenomenology/tsallis_issues_"),
    )
    ratio = cs.Clone()
    ratio.Divide(tsallis)
    plot(
        [ratio],
        stop=stop,
        logy=False,
        ytitle=invariant_cross_section_code(),
        xtitle="p_{T} (GeV/#it{c})",
        # xlimits=(0.7, 22),
        csize=(96, 128),
        ltitle=ltitle,
        legend_pos=(0.65, 0.7, 0.8, 0.88),
        yoffset=1.4,
        more_logs=False,
        oname=oname.format("phenomenology/tsallis_"),
    )


@pytest.fixture
def pars():
    with open("config/predictions/tsallis-pion.json") as f:
        data = json.load(f)
    return pd.DataFrame(data.values())


@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    # "#eta",
])
@pytest.mark.parametrize("parameter", [
    "n",
    "C"
])
def test_tsallis_parameter_dependence(pars, parameter, stop, ltitle, oname):
    print(pars)
    graph = br.graph(
        "test",
        pars["energy"],
        pars[parameter],
        np.zeros_like(pars["energy"]),
        pars["d{}".format(parameter)])
    graph.SetMarkerColor(4)
    graph.SetMarkerStyle(21)

    plot(
        [graph],
        stop=stop,
        logy=False,
        ytitle=parameter,
        xtitle="#sqrt{s} (GeV)",
        xlimits=(0.8, 14),
        csize=(96, 128),
        ltitle=ltitle,
        legend_pos=(0.65, 0.7, 0.8, 0.88),
        yoffset=1.4,
        oname=oname.format("phenomenology/tsallis_"),
    )
