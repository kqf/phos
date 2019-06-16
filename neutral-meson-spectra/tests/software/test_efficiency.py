import pytest

from lazy_object_proxy import Proxy
from spectrum.efficiency import Efficiency
from vault.datavault import DataVault
from spectrum.options import EfficiencyOptions
from spectrum.options import CompositeEfficiencyOptions
from spectrum.output import open_loggs
from spectrum.comparator import Comparator

MC_DATA = Proxy(
    lambda: DataVault().input("pythia8")
)

SPMC_DATA = Proxy(
    lambda: (
        DataVault().input("single #pi^{0}", "low", "PhysEff"),
        DataVault().input("single #pi^{0}", "high", "PhysEff"),
    )
)


@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("name, options, data", [
    ("simple", EfficiencyOptions(), MC_DATA),
    ("composite", CompositeEfficiencyOptions("#pi^{0}"), SPMC_DATA),
])
def test_efficiency(name, options, data):
    estimator = Efficiency(options)
    with open_loggs("test {} efficiency".format(name)) as loggs:
        efficiency = estimator.transform(data, loggs)

    Comparator().compare(efficiency)
    assert efficiency.GetEntries() > 0
