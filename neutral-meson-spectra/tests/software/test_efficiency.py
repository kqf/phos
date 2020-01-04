import pytest

from spectrum.efficiency import Efficiency
from spectrum.efficiency import simple_efficiency_data, efficiency_data
from spectrum.options import EfficiencyOptions
from spectrum.options import CompositeEfficiencyOptions
from spectrum.output import open_loggs
from spectrum.comparator import Comparator


@pytest.fixture
def data(name):
    if name == "simple":
        return simple_efficiency_data()
    return efficiency_data()


@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("name, options", [
    ("simple", EfficiencyOptions()),
    ("composite", CompositeEfficiencyOptions("#pi^{0}")),
])
def test_efficiency(name, options, data):
    estimator = Efficiency(options)
    with open_loggs("test {} efficiency".format(name)) as loggs:
        efficiency = estimator.transform(data, loggs)

    Comparator().compare(efficiency)
    assert efficiency.GetEntries() > 0
