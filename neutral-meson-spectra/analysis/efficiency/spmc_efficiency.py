import pytest

from lazy_object_proxy import Proxy
from spectrum.efficiency import Efficiency
from spectrum.options import CompositeEfficiencyOptions
from spectrum.output import AnalysisOutput
from spectrum.broot import BROOT as br
from spectrum.comparator import Comparator  # noqa

from tools.validate import validate
from vault.datavault import DataVault

PION_INPUT = Proxy(
    lambda:
    (
        DataVault().input("single #pi^{0}", "low", "PhysEff"),
        DataVault().input("single #pi^{0}", "high", "PhysEff"),
    )
)

ETA_INPUT = Proxy(
    lambda:
    (
        DataVault().input("single #eta", "low"),
        DataVault().input("single #eta", "high"),
    )
)


@pytest.mark.onlylocal
@pytest.mark.parametrize("data, particle", [
    (PION_INPUT, "#pi^{0}"),
    (ETA_INPUT, "#eta"),
])
def test_spmc_efficiency(data, particle):
    options = CompositeEfficiencyOptions(particle)
    loggs = AnalysisOutput("efficiency_spmc_{}".format(particle))
    efficiency = Efficiency(options).transform(data, loggs)
    # validate(br.hist2dict(efficiency), "spmc_efficiency/" + particle)
    Comparator().compare(efficiency)
    return efficiency
