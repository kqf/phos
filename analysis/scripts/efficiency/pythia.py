import pytest

from spectrum.efficiency import Efficiency, simple_efficiency_data
from spectrum.options import EfficiencyOptions
from spectrum.output import open_loggs
from spectrum.comparator import Comparator  # noqa


@pytest.fixture
def pythia(particle):
    return simple_efficiency_data(particle=particle)


@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta",
])
def test_efficiency(pythia, particle):
    options = EfficiencyOptions(particle)
    with open_loggs() as loggs:
        efficiency = Efficiency(options).transform(pythia, loggs)
        Comparator().compare(efficiency)
