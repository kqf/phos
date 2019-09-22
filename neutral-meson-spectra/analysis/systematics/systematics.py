import pytest
from spectrum.uncertainties.total import uncertainties
from spectrum.uncertainties.total import data_total_uncert
from spectrum.uncertainties.total import TotalUncertainty
from spectrum.uncertainties.total import TotalUncertaintyOptions
from spectrum.output import open_loggs

from spectrum.comparator import Comparator


@pytest.fixture
def dataset(particle):
    return data_total_uncert(particle)


@pytest.mark.skip("")
@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.interactive
def test_draws_all_sources(dataset):
    # with open_loggs() as loggs:
    Comparator().compare(uncertainties("#pi^{0}", dataset))


@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle", [
    # "#pi^{0}",
    "#eta",
])
def test_calculates_total_uncertainty(particle, dataset):
    with open_loggs() as loggs:
        tot = TotalUncertainty(TotalUncertaintyOptions(particle=particle))
        Comparator().compare(tot.transform(dataset, loggs))
