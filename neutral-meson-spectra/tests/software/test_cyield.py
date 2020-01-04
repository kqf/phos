import pytest

from spectrum.options import CompositeCorrectedYieldOptions
from spectrum.options import CorrectedYieldOptions
from spectrum.cyield import CorrectedYield, cyield_data, simple_cyield_data
from spectrum.output import open_loggs


@pytest.fixture
def cdata():
    return cyield_data(particle="#pi^{0}")


@pytest.fixture
def simple_cdata():
    return simple_cyield_data(particle="#pi^{0}")


@pytest.mark.onlylocal
def test_corrected_yield(simple_cdata):
    estimator = CorrectedYield(
        CorrectedYieldOptions(particle="#pi^{0}")
    )
    with open_loggs() as loggs:
        estimator.transform(simple_cdata, loggs)


@pytest.mark.onlylocal
def test_composite_yield(cdata):
    estimator = CorrectedYield(
        CompositeCorrectedYieldOptions(particle="#pi^{0}")
    )
    with open_loggs() as loggs:
        estimator.transform(cdata, loggs)
