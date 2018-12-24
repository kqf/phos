import pytest

from lazy_object_proxy import Proxy
from spectrum.options import CompositeCorrectedYieldOptions
from spectrum.options import CorrectedYieldOptions
from spectrum.corrected_yield import CorrectedYield

from vault.datavault import DataVault
from tools.feeddown import data_feeddown

YIELD_DATA = Proxy(
    lambda: (
        DataVault().input("data", histname="MassPtSM0"),
        data_feeddown(),
    )
)

PYTHIA8_DATA = Proxy(
    lambda: (
        YIELD_DATA,
        DataVault().input("pythia8"),
    )
)
SPMC_DATA = Proxy(
    lambda: (
        YIELD_DATA, (
            DataVault().input("single #pi^{0}", "low", "PhysEff"),
            DataVault().input("single #pi^{0}", "high", "PhysEff"),
        )
    )
)


@pytest.mark.onlylocal
def test_corrected_yield():
    estimator = CorrectedYield(
        CorrectedYieldOptions(particle="#pi^{0}")
    )
    estimator.transform(PYTHIA8_DATA, {})


@pytest.mark.onlylocal
def test_composite_yield():
    estimator = CorrectedYield(
        CompositeCorrectedYieldOptions(particle="#pi^{0}")
    )
    estimator.transform(SPMC_DATA, {})
