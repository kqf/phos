import pytest

from spectrum.output import open_loggs
from spectrum.options import Options, CompositeOptions
from spectrum.analysis import Analysis
from vault.datavault import DataVault


@pytest.fixture
def data():
    return DataVault().input("data", histname="MassPtSM0")


@pytest.fixture
def data_spmc():
    return (
        DataVault().input("single #pi^{0}", "low", "PhysEff"),
        DataVault().input("single #pi^{0}", "high", "PhysEff"),
    )


@pytest.mark.onlylocal
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    # "#eta",
])
def test_simple(particle, data):
    analysis = Analysis(Options(particle=particle))
    with open_loggs("test the single analysis") as loggs:
        output = analysis.transform(data, loggs=loggs)
    assert len(output) > 0


@pytest.mark.onlylocal
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    # "#eta",
])
def test_composite(particle, data_spmc):
    analysis = Analysis(CompositeOptions(particle=particle))
    with open_loggs("test the composite analysis") as loggs:
        output = analysis.transform(data_spmc, loggs=loggs)
    assert len(output) > 0
