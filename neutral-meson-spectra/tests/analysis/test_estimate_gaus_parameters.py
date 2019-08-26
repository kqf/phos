import pytest

from spectrum.output import open_loggs
from spectrum.options import Options
from spectrum.analysis import Analysis
from spectrum.pipeline import ComparePipeline
from vault.datavault import DataVault


@pytest.fixture
def data():
    return [
        # DataVault().input("data", histname="MassPtSM0"),
        DataVault().input("data", histname="MassPtSM0"),
    ]


@pytest.fixture
def options(particle):
    return {
        # "gaus": Options(particle=particle, signal="config/data/cball.json"),
        "cball": Options(
            particle=particle,
            signal="config/data/gaus.json",
            background="config/data/gaus.json"
        ),
    }


@pytest.mark.onlylocal
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    # "#eta",
])
def test_simple(particle, data, options):
    estimator = ComparePipeline([
        (name, Analysis(options[name]))
        for name in options
    ])
    with open_loggs("estimate gaus parameters") as loggs:
        estimator.transform(data, loggs=loggs)
