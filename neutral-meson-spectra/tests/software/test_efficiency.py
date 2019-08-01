import pytest

from spectrum.efficiency import Efficiency
from vault.datavault import DataVault
from spectrum.options import EfficiencyOptions
from spectrum.options import CompositeEfficiencyOptions
from spectrum.output import open_loggs
from spectrum.comparator import Comparator


def mc_data():
    return DataVault().input("pythia8")


def spmc_data():
    return (
        DataVault().input("single #pi^{0}", "low", "PhysEff"),
        DataVault().input("single #pi^{0}", "high", "PhysEff"),
    )


@pytest.fixture
def data(name):
    return {
        "simple": mc_data(),
        "composite": spmc_data(),
    }.get(name)


@pytest.mark.parametrize("name, options", [
    ("simple", EfficiencyOptions()),
    ("composite", CompositeEfficiencyOptions("#pi^{0}")),
])
@pytest.mark.interactive
@pytest.mark.onlylocal
def test_efficiency(name, options, data):
    estimator = Efficiency(options)
    with open_loggs("test {} efficiency".format(name)) as loggs:
        efficiency = estimator.transform(data, loggs)

    Comparator().compare(efficiency)
    assert efficiency.GetEntries() > 0
