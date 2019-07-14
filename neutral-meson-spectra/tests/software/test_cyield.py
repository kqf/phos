import pytest

from spectrum.options import CompositeCorrectedYieldOptions
from spectrum.options import CorrectedYieldOptions
from spectrum.corrected_yield import CorrectedYield
from spectrum.output import open_loggs

from vault.datavault import DataVault
from tools.feeddown import data_feeddown


@pytest.fixture
def raw_yield_data():
    return (
        DataVault().input("data", histname="MassPtSM0"),
        data_feeddown(),
    )


@pytest.fixture
def pythia_data(raw_yield_data):
    return (
        raw_yield_data,
        DataVault().input("pythia8"),
    )


@pytest.fixture
def spmc_data(raw_yield_data):
    return (
        raw_yield_data,
        (
            DataVault().input("single #pi^{0}", "low", "PhysEff"),
            DataVault().input("single #pi^{0}", "high", "PhysEff"),
        )
    )



@pytest.mark.onlylocal
def test_corrected_yield(pythia_data):
    estimator = CorrectedYield(
        CorrectedYieldOptions(particle="#pi^{0}")
    )
    with open_loggs() as loggs:
        estimator.transform(pythia_data, loggs)


@pytest.mark.onlylocal
def test_composite_yield(spmc_data):
    estimator = CorrectedYield(
        CompositeCorrectedYieldOptions(particle="#pi^{0}")
    )
    with open_loggs() as loggs:
        estimator.transform(spmc_data, loggs)
