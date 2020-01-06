import pytest
from spectrum.vault import DataVault
from spectrum.cyield import cyield_data as cyield
from spectrum.efficiency import efficiency_data


@pytest.fixture
def ltitle(particle):
    return "{} #rightarrow #gamma #gamma".format(particle)


@pytest.fixture
def data():
    return DataVault().input("data", histname="MassPtSM0")


@pytest.fixture
def cyield_data(particle):
    return cyield(particle)


@pytest.fixture
def spmc(particle):
    return efficiency_data(particle)
