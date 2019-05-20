import pytest

from lazy_object_proxy import Proxy
from spectrum.efficiency import Efficiency
from vault.datavault import DataVault
from spectrum.options import EfficiencyOptions
from spectrum.options import CompositeEfficiencyOptions
from spectrum.output import AnalysisOutput
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
def test_simple(name, options, data):
    loggs = AnalysisOutput("test {} efficiency".format(name))
    efficiency = Efficiency(options).transform(data, loggs=loggs)
    Comparator().compare(efficiency)
    # loggs.plot()
    assert efficiency.GetEntries() > 0
