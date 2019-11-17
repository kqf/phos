import ROOT
import pytest

import spectrum.broot as br
from spectrum.output import open_loggs
from spectrum.options import Options
from spectrum.analysis import Analysis
from spectrum.pipeline import ParallelPipeline
from spectrum.plotter import plot
from vault.datavault import DataVault


@pytest.fixture
def calibration_data(particle, spmc, data, quant):
    data = [data] + list(spmc)
    labels = "Data", "Low p_{T}", "High p_{T}"
    scales = [1, 1.0189, 1.0189]
    with open_loggs() as loggs:
        estimator = ParallelPipeline([
            (label, Analysis(Options(particle)))
            for label in labels
        ])
        output = estimator.transform(data, loggs)
        targets = []
        for name, hists, s in zip(labels, output, scales):
            hist = hists._asdict()[quant]
            if quant == "mass":
                hist.Scale(s)
            hist.SetTitle(name)
            targets.append(br.hist2graph(hist, "positive"))
    return targets


@pytest.fixture
def spmc(particle):
    production = "single {}".format(particle)
    return (
        DataVault().input(production, "low", "PhysEff"),
        DataVault().input(production, "high", "PhysEff"),
    )


@pytest.fixture
def data():
    return DataVault().input("data", histname="MassPtSM0")


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
def test_mass_width_parametrization(calibration_data, quant, oname, ltitle):
    plot(
        calibration_data,
        oname=oname,
        ltitle=ltitle,
        logy=False,
        yoffset=1.8
    )
