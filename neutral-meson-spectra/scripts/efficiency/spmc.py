import pytest

from spectrum.efficiency import Efficiency
from spectrum.options import CompositeEfficiencyOptions
from spectrum.output import open_loggs
import spectrum.broot as br  # noqa
from spectrum.comparator import Comparator  # noqa

from spectrum.tools.validate import validate  # noqa
from spectrum.plotter import plot


@pytest.fixture
def oname(particle):
    pattern = "results/analysis/spmc/efficiency_{}.pdf"
    return pattern.format(br.spell(particle))


@pytest.mark.onlylocal
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta",
])
@pytest.mark.parametrize("logname", [
    "",
    # "efficiency-{}",
])
def test_spmc_efficiency(particle, efficiency_data, oname, logname):
    options = CompositeEfficiencyOptions(particle)
    with open_loggs(logname.format(particle)) as loggs:
        efficiency = Efficiency(options).transform(efficiency_data, loggs)
        # validate(br.hist2dict(efficiency), "spmc_efficiency/" + particle)
        # Comparator().compare(efficiency)
        plot(
            [efficiency],
            logy=False,
            logx=False,
            oname=oname,
            legend_pos=None,
            yoffset=2
        )
