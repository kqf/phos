import pytest

from spectrum.output import open_loggs
from spectrum.analysis import Analysis
from vault.datavault import DataVault
from tools.feeddown import data_feeddown
from spectrum.options import Options
from spectrum.corrected_yield import CorrectedYield
from spectrum.options import CompositeCorrectedYieldOptions
from spectrum.efficiency import Efficiency
from spectrum.options import CompositeEfficiencyOptions


from spectrum.comparator import Comparator


@pytest.fixture
def data():
    return DataVault().input("data", histname="MassPtSM0")


@pytest.fixture
def yield_data(data):
    return data, data_feeddown()


def pion_data():
    return (
        DataVault().input("single #pi^{0}", "low", "PhysEff"),
        DataVault().input("single #pi^{0}", "high", "PhysEff"),
    )


def eta_data():
    return (
        DataVault().input("single #eta", "low", "PhysEff"),
        DataVault().input("single #eta", "high", "PhysEff"),
    )


@pytest.fixture
def mc(particle):
    return {
        "#pi^{0}": pion_data(),
        "#eta": eta_data(),
    }.get(particle)


@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle, spmc", [
    "#pi^{0}",
    "#eta",
])
def test_simple(particle, mc, data, yield_data):
    estimator = Analysis(Options(particle=particle))
    with open_loggs("simple test") as loggs:
        meson = estimator.transform(data, loggs)

        estimator = Efficiency(CompositeEfficiencyOptions(particle=particle))
        efficiency = estimator.transform(mc, loggs)

        estimator = CorrectedYield(
            CompositeCorrectedYieldOptions(particle="#pi^{0}")
        )
        corr_meson = estimator.transform((yield_data, mc), loggs)
        Comparator().compare([meson, efficiency, corr_meson])
