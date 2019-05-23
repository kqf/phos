import pytest

from lazy_object_proxy import Proxy
from spectrum.efficiency import Efficiency
from spectrum.options import EfficiencyOptions
from spectrum.output import AnalysisOutput
# from spectrum.broot import BROOT as br
from spectrum.comparator import Comparator  # noqa

# from tools.validate import validate
from vault.datavault import DataVault

DATASET = Proxy(
    lambda: DataVault().input("pythia8", listname="PhysEff")
)


@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.parametrize("data, particle", [
    (DATASET, "#pi^{0}"),
    # (ETA_INPUT, "#eta"),
])
def test_efficiency(data, particle):
    options = EfficiencyOptions(particle)
    loggs = AnalysisOutput("efficiency_spmc_{}".format(particle))
    efficiency = Efficiency(options).transform(data, loggs)
    # validate(br.hist2dict(efficiency), "spmc_efficiency/" + particle)
    Comparator().compare(efficiency)
    return efficiency
