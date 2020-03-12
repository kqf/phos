import pytest

from spectrum.efficiency import Efficiency
from spectrum.comparator import Comparator
from spectrum.vault import DataVault
from spectrum.output import open_loggs
from spectrum.options import EfficiencyOptions


@pytest.fixture
def data(particle):
    return {
        "#eta": DataVault().input("single #eta", "high", "PhysEff"),
        "#pi^{0}": DataVault().input("single #pi^{0}", "high", "PhysEff"),
    }.get(particle)


@pytest.fixture
def edges():
    return [
        6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0, 10.5, 11.0, 11.5,
        12.0, 12.5, 13.0, 13.5, 14.0, 14.5, 15.0, 15.5, 16.0, 16.5, 17.0,
        17.5, 18.0, 18.5, 19.0, 19.5, 20.0
    ]


@pytest.fixture
def rebins():
    return [0] * (len(edges) - 1)


@pytest.fixture
def options(edges, rebins):
    options = EfficiencyOptions()
    options.analysis.pt.ptedges = edges
    options.analysis.pt.rebins = rebins
    options.analysis.invmass.use_mixed = False
    return options


@pytest.mark.onlylocal
@pytest.mark.parametrize("particle", ["#pi^{0}", "#eta"])
def test_high_momentum(particle, data, options):
    with open_loggs("test high momentum {}".format(particle)) as loggs:
        efficiency = Efficiency(options).transform(data, loggs)
        efficiency.SetTitle('Efficiency at high #it{p}_{T}')
        Comparator().compare(efficiency)
