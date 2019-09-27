import pytest

from spectrum.output import open_loggs
from spectrum.pipeline import ComparePipeline, HistogramSelector, Pipeline
from spectrum.options import Options
from spectrum.analysis import Analysis
from vault.datavault import DataVault


@pytest.fixture
def old_new_data():
    return (
        DataVault().input("data", "tof", histname="MassPtSM0"),
        DataVault().input("data", histname="MassPtSM0"),
    )


@pytest.fixture
def data():
    return (
        DataVault().input("data", "latest LHC16", histname="MassPtSM0"),
        DataVault().input("data", "latest LHC17", histname="MassPtSM0"),
        DataVault().input("data", "latest LHC18", histname="MassPtSM0"),
    )


def analysis(particle):
    return Pipeline([
        ("analysis", Analysis(Options(particle=particle))),
        ("spectrum", HistogramSelector("spectrum")),
    ])


@pytest.mark.skip()
@pytest.mark.onlylocal
@pytest.mark.parametrize("particle", [
    # "#pi^{0}",
    "#eta",
])
def test_old_new(particle, old_new_data):
    estimator = ComparePipeline([
        ("old", analysis(particle)),
        ("new", analysis(particle)),
    ], plot=True)
    with open_loggs("old-reports-{}".format(particle)) as loggs:
        estimator.transform(old_new_data, loggs)


@pytest.mark.onlylocal
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    # "#eta",
])
def test_periods(particle, data):
    estimator = ComparePipeline([
        ("LHC16", analysis(particle)),
        ("LHC17", analysis(particle)),
        ("LHC18", analysis(particle)),
    ], plot=True)
    with open_loggs("reports-{}".format(particle)) as loggs:
        estimator.transform(data, loggs)
