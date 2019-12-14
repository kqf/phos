import pytest
from vault.datavault import DataVault
from spectrum.corrected_yield import data_cyield as cyield


@pytest.fixture
def ltitle(particle):
    return "{} #rightarrow #gamma #gamma".format(particle)


@pytest.fixture
def data():
    return DataVault().input("data", histname="MassPtSM0")


@pytest.fixture
def data_cyield(particle):
    return cyield(particle)


@pytest.fixture
def spmc(particle):
    production = "single {}".format(particle)
    return (
        DataVault().input(production, "low", "PhysEff"),
        DataVault().input(production, "high", "PhysEff"),
    )
