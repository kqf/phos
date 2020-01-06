import pytest

from spectrum.output import open_loggs
from spectrum.options import Options
from spectrum.analysis import Analysis
from spectrum.pipeline import ComparePipeline, Pipeline, HistogramSelector
from spectrum.vault import DataVault


@pytest.fixture
def data():
    return [
        DataVault().input("data", histname="MassPtSM0"),
        DataVault().input("data", histname="MassPtSM0"),
    ]


@pytest.fixture
def options(particle):
    return {
        "cball": Options(particle=particle),
        "gaus": Options(
            particle=particle,
            signal="config/data/gaus.json",
            background="config/data/gaus.json"
        ),
    }


def spectrum_pipeline(options):
    return Pipeline([
        ("analysis", Analysis(options)),
        ("spectrum", HistogramSelector("spectrum")),
    ])


@pytest.mark.onlylocal
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    # "#eta",
])
def test_simple(particle, data, options):
    for option in options.values():
        option.calibration.nsigmas = 3
        option.invmass.signal.background = "pol1"
        option.invmass.signal.fit_range = [0.04, 0.20]
        option.invmass.background.fit_range = [0.04, 0.20]

    estimator = ComparePipeline([
        (name, spectrum_pipeline(options[name]))
        for name in options
    ])
    with open_loggs("estimate gaus parameters") as loggs:
        estimator.transform(data, loggs=loggs)
