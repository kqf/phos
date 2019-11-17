import pytest

from spectrum.efficiency import Efficiency
from spectrum.options import CompositeEfficiencyOptions
from spectrum.output import open_loggs
import spectrum.broot as br  # noqa
from spectrum.comparator import Comparator  # noqa

from spectrum.tools.validate import validate  # noqa
from vault.datavault import DataVault
from spectrum.plotter import plot


@pytest.fixture
def data(particle):
    production = "single {}".format(particle)
    return (
        DataVault().input(production, "low", "PhysEff"),
        DataVault().input(production, "high", "PhysEff"),
    )


@pytest.mark.onlylocal
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta",
])
def test_spmc_efficiency(particle, data):
    options = CompositeEfficiencyOptions(particle)
    with open_loggs() as loggs:
        efficiency = Efficiency(options).transform(data, loggs)
        # validate(br.hist2dict(efficiency), "spmc_efficiency/" + particle)
        # Comparator().compare(efficiency)
        plot(
            [efficiency],
            logy=False,
            logx=False,
            legend_pos=None,
            yoffset=2
        )
