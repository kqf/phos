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


@pytest.fixture
def data(particle, raw_data, quant):
    labels = "Data", "Low #it{p}_{T}", "High #it{p}_{T}"
    scales = [1, 1.0189, 1.0189]
    with open_loggs() as loggs:
        estimator = ParallelPipeline([
            (label, Analysis(Options(particle)))
            for label in labels
        ])
        output = estimator.transform(raw_data, loggs)
        targets = []
        for name, hists, s in zip(labels, output, scales):
            hist = hists._asdict()[quant]
            if quant == "mass":
                hist.Scale(s)
            hist.SetTitle(name)
            targets.append(br.hist2graph(hist, "positive"))
    return targets


@pytest.fixture
def ltitle(particle):
    return "{} #rightarrow #gamma#gamma".format(particle)


@pytest.fixture
def oname(particle, quant):
    return "results/analysis/spmc/{}_{}.pdf".format(quant, br.spell(particle))


@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta",
])
@pytest.mark.parametrize("quant", [
    "mass",
    "width",
])
def test_mass_width_parametrization(data, quant, stop, oname, ltitle):
    plot(
        data,
        stop=stop,
        oname=oname,
        ltitle=ltitle,
        logy=False,
        yoffset=1.8
    )
