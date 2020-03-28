import pytest

from spectrum.options import CompositeCorrectedYieldOptions
from spectrum.options import CorrectedYieldOptions
from spectrum.cyield import CorrectedYield, cyield_data, simple_cyield_data
from spectrum.output import open_loggs


@pytest.fixture
def cdata(particle):
    return cyield_data(particle=particle)


@pytest.fixture
def simple_cdata(particle):
    return simple_cyield_data(particle=particle)


@pytest.mark.onlylocal
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta",
])
def test_corrected_yield(simple_cdata, particle):
    estimator = CorrectedYield(
        CorrectedYieldOptions(particle=particle)
    )
    with open_loggs() as loggs:
        estimator.transform(simple_cdata, loggs)


@pytest.mark.onlylocal
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta",
])
def test_composite_yield(cdata, particle):
    estimator = CorrectedYield(
        CompositeCorrectedYieldOptions(particle=particle)
    )
    with open_loggs() as loggs:
        estimator.transform(cdata, loggs)
