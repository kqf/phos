import pytest

import spectrum.broot as br
from spectrum.output import open_loggs
from spectrum.pipeline import ComparePipeline,
from spectrum.pipeline import ParallelPipeline, HistogramSelector, Pipeline
from spectrum.options import Options
from spectrum.analysis import Analysis
from vault.datavault import DataVault
from spectrum.plotter import plot


@pytest.fixture
def old_new_data():
    return (
        DataVault().input("data", "staging", histname="MassPtSM0"),
        DataVault().input("data", histname="MassPtSM0"),
    )


@pytest.fixture
def data():
    return (
        DataVault().input("data", "staging LHC16", histname="MassPtSM0"),
        DataVault().input("data", "staging LHC17", histname="MassPtSM0"),
        DataVault().input("data", "staging LHC18", histname="MassPtSM0"),
    )


def analysis(particle, quant="mass"):
    return Pipeline([
        ("analysis", Analysis(Options(particle=particle))),
        ("spectrum", HistogramSelector(quant)),
    ])


@pytest.mark.skip()
@pytest.mark.onlylocal
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    # "#eta",
])
def test_old_new(particle, old_new_data):
    estimator = ComparePipeline([
        ("old", analysis(particle)),
        ("new", analysis(particle)),
    ], plot=True)
    with open_loggs("old-reports-{}".format(particle)) as loggs:
        estimator.transform(old_new_data, loggs)


@pytest.fixture
def oname(particle, quant):
    return "results/{}_{}.pdf".format(quant, br.spell(particle))


@pytest.mark.onlylocal
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    # "#eta",
])
@pytest.mark.parametrize("quant", [
    "mass",
    # "width",
    # "spectrum",
])
def test_periods(particle, data, quant, oname):
    labels = "LHC16", "LHC17", "LHC18"

    estimator = ParallelPipeline([
        (l, analysis(particle, quant))
        for l in labels
    ])
    with open_loggs("particles") as loggs:
        hists = estimator.transform(data, loggs)
        for hist, label in zip(hists, labels):
            hist.SetTitle(label)
        plot(hists, logy=False, oname=oname)
