import pytest
from spectrum.efficiency import efficiency_data
from vault.datavault import DataVault


@pytest.fixture
def ltitle(particle):
    return "{} #rightarrow #gamma #gamma".format(particle)


@pytest.fixture
def data():
    return DataVault().input("data", histname="MassPtSM0")


@pytest.fixture
def spmc(particle):
    return efficiency_data(particle)
