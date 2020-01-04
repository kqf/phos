import pytest

from spectrum.efficiency import Efficiency
from spectrum.efficiency import simple_efficiency_data, efficiency_data
from spectrum.options import EfficiencyOptions
from spectrum.options import CompositeEfficiencyOptions
from spectrum.output import open_loggs
from spectrum.comparator import Comparator


@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("name, options, data", [
    ("simple", EfficiencyOptions(), simple_efficiency_data()),
    ("composite", CompositeEfficiencyOptions("#pi^{0}"), efficiency_data()),
])
def test_efficiency(name, options, data):
    estimator = Efficiency(options)
    with open_loggs("test {} efficiency".format(name)) as loggs:
        efficiency = estimator.transform(data, loggs)

    Comparator().compare(efficiency)
    assert efficiency.GetEntries() > 0
