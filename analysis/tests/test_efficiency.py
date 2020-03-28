import pytest

from spectrum.efficiency import Efficiency
from spectrum.efficiency import simple_efficiency_data, efficiency_data
from spectrum.options import EfficiencyOptions
from spectrum.options import CompositeEfficiencyOptions
from spectrum.output import open_loggs


@pytest.fixture
def sdata():
    return simple_efficiency_data()


@pytest.fixture
def cdata():
    return efficiency_data()


@pytest.mark.onlylocal
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta",
])
def test_efficiency(particle, sdata):
    estimator = Efficiency(EfficiencyOptions(particle))
    with open_loggs() as loggs:
        efficiency = estimator.transform(sdata, loggs)
    assert efficiency.GetEntries() > 0


@pytest.mark.onlylocal
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta",
])
def test_composite_efficiency(particle, cdata):
    estimator = Efficiency(CompositeEfficiencyOptions(particle))
    with open_loggs() as loggs:
        efficiency = estimator.transform(cdata, loggs)
    assert efficiency.GetEntries() > 0
