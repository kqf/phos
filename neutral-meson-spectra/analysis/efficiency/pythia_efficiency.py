import pytest

from spectrum.efficiency import Efficiency
from spectrum.options import EfficiencyOptions
from spectrum.output import open_loggs
# import spectrum.broot as br
from spectrum.comparator import Comparator  # noqa

# from spectrum.tools.validate import validate
from vault.datavault import DataVault


@pytest.fixture
def data():
    return DataVault().input("pythia8", listname="PhysEff")


@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta",
])
def test_efficiency(data, particle):
    options = EfficiencyOptions(particle)
    with open_loggs("efficiency pytia8 {}".format(particle)) as loggs:
        efficiency = Efficiency(options).transform(data, loggs)
        Comparator().compare(efficiency)
