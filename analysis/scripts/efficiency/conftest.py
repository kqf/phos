import pytest
import spectrum.broot as br

from spectrum.efficiency import efficiency_data as edata
from spectrum.vault import DataVault


@pytest.fixture
def ltitle(particle):
    return "{} #rightarrow #gamma #gamma".format(particle)


@pytest.fixture
def data():
    return DataVault().input("data", histname="MassPtSM0")


@pytest.fixture
def spmc(particle):
    prod = "single {}".format(particle)
    return (
        DataVault().input(prod, "low", "PhysEff"),
        DataVault().input(prod, "high", "PhysEff"),
    )


@pytest.fixture
def efficiency_data(particle):
    return edata(particle)


@pytest.fixture
def oname(particle, target):
    pattern = "images/analysis/spmc/{}_{}.pdf"
    return pattern.format(target, br.spell(particle))
