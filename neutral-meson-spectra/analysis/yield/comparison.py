import pytest

from lazy_object_proxy import Proxy
from spectrum.output import AnalysisOutput # noqa
from spectrum.analysis import Analysis
from vault.datavault import DataVault
from tools.feeddown import data_feeddown
from spectrum.options import CompositeOptions
from spectrum.corrected_yield import CorrectedYield
from spectrum.options import CompositeCorrectedYieldOptions
from spectrum.efficiency import Efficiency
from spectrum.options import CompositeEfficiencyOptions


from spectrum.comparator import Comparator

INPUT_DATA = Proxy(
    lambda: DataVault().input("data", histname="MassPtSM0")
)

YIELD_DATA = Proxy(
    lambda: (
        INPUT_DATA,
        data_feeddown(),
    )
)

SPMC_PION = Proxy(
    lambda: (
        DataVault().input("single #pi^{0}", "low", "PhysEff"),
        DataVault().input("single #pi^{0}", "high", "PhysEff"),
    )
)


@pytest.mark.onlylocal
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    # "#eta",
])
def test_simple(particle):
    estimator = Analysis(CompositeOptions(particle=particle))
    pion = estimator.transform(INPUT_DATA, {})

    estimator = Efficiency(CompositeEfficiencyOptions(particle=particle))
    efficiency = estimator.transform(SPMC_PION, {})

    estimator = CorrectedYield(
        CompositeCorrectedYieldOptions(particle="#pi^{0}")
    )
    ypion = estimator.transform((YIELD_DATA, SPMC_PION), {})
    Comparator().compare([pion, efficiency, ypion])
