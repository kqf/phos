import pytest

from spectrum.efficiency import Efficiency
from spectrum.options import CompositeEfficiencyOptions
from spectrum.output import open_loggs
import spectrum.broot as br  # noqa
from spectrum.comparator import Comparator  # noqa

from spectrum.tools.validate import validate  # noqa
from vault.datavault import DataVault


def pion_data():
    return (
        DataVault().input("single #pi^{0}", "low", "PhysEff"),
        DataVault().input("single #pi^{0}", "high", "PhysEff"),
    )


def eta_data():
    return (
        DataVault().input("single #eta", "low"),
        DataVault().input("single #eta", "high"),
    )


@pytest.fixture
def data(particle):
    return {
        "#pi^{0}": pion_data(),
        "#eta": eta_data(),

    }.get(particle)


@pytest.mark.onlylocal
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta",
])
def test_spmc_efficiency(particle, data):
    options = CompositeEfficiencyOptions(particle)
    # with open_loggs("efficiency spmc {}".format(particle)) as loggs:
    with open_loggs() as loggs:
        efficiency = Efficiency(options).transform(data, loggs)
        validate(br.hist2dict(efficiency), "spmc_efficiency/" + particle)
        # Comparator().compare(efficiency)
