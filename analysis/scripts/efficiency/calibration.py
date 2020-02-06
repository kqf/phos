import pytest

import spectrum.broot as br
from spectrum.output import open_loggs
from spectrum.options import Options
from spectrum.analysis import Analysis
from spectrum.pipeline import ParallelPipeline
from spectrum.plotter import plot
from spectrum.vault import DataVault


@pytest.fixture
def raw_data(particle):
    prod = "single {}".format(particle)
    return (
        DataVault().input("data", histname="MassPtSM0"),
        DataVault().input(prod, "low", "PhysEff"),
        DataVault().input(prod, "high", "PhysEff"),
    )


def trimm(a, b):
    def f(x, y, dx, dy):
        idx = (a < x) & (x < b)
        return x[idx], y[idx], dx[idx], dy[idx]
    return f


@pytest.fixture
def data(particle, raw_data, target):
    labels = "Data", "Low #it{p}_{T}", "High #it{p}_{T}"
    scales = [1, 1.0189, 1.0189]
    pt_ranges = [(0, 20), (0, 8), (5, 20)]
    with open_loggs() as loggs:
        estimator = ParallelPipeline([
            (label, Analysis(Options(particle)))
            for label in labels
        ])
        output = estimator.transform(raw_data, loggs)
        targets = []
        for name, hists, s, pt in zip(labels, output, scales, pt_ranges):
            hist = hists._asdict()[target]
            if target == "mass":
                hist.Scale(s)
            hist.SetTitle(name)
            targets.append(br.hist2graph(hist, func=trimm(*pt)))
    return targets


@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta",
])
@pytest.mark.parametrize("target", [
    "mass",
    "width",
])
def test_mass_width_parametrization(data, stop, oname, ltitle):
    plot(
        data,
        stop=stop,
        oname=oname,
        ltitle=ltitle,
        logy=False,
        yoffset=2,
    )
