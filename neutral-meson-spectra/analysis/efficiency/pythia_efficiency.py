import pytest

from spectrum.efficiency import Efficiency
from spectrum.options import EfficiencyOptions
from spectrum.output import open_loggs
from spectrum.comparator import Comparator  # noqa
from vault.datavault import DataVault


@pytest.fixture
def pythia():
    return DataVault().input("pythia8", listname="PhysEff")


@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta",
])
def test_efficiency(pythia, particle):
    options = EfficiencyOptions(particle)
    with open_loggs("efficiency pytia8 {}".format(particle)) as loggs:
        efficiency = Efficiency(options).transform(pythia, loggs)
        Comparator().compare(efficiency)
