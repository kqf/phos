import pytest

from lazy_object_proxy import Proxy
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


SPMC_PION = Proxy(
    lambda: (
        DataVault().input("single #pi^{0}", "low", "PhysEff"),
        DataVault().input("single #pi^{0}", "high", "PhysEff"),
    )
)


SPMC_ETA = Proxy(
    lambda: (
        DataVault().input("single #eta", "low", "PhysEff"),
        DataVault().input("single #eta", "high", "PhysEff"),
    )
)


@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle, spmc", [
    ("#pi^{0}", SPMC_PION),
    ("#eta", SPMC_ETA),
])
def test_simple(particle, spmc, data, yield_data):
    estimator = Analysis(Options(particle=particle))
    with open_loggs("simple test", save=False) as loggs:
        meson = estimator.transform(data, loggs)

        estimator = Efficiency(CompositeEfficiencyOptions(particle=particle))
        efficiency = estimator.transform(spmc, loggs)

        estimator = CorrectedYield(
            CompositeCorrectedYieldOptions(particle="#pi^{0}")
        )
        corr_meson = estimator.transform((yield_data, spmc), loggs)
        Comparator().compare([meson, efficiency, corr_meson])
