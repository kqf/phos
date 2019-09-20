import pytest
from spectrum.uncertainties.total import uncertainties
from spectrum.uncertainties.total import data
from spectrum.uncertainties.total import TotalUncertainty
from spectrum.uncertainties.total import TotalUncertaintyOptions
from spectrum.output import open_loggs

from spectrum.comparator import Comparator


@pytest.fixture
def dataset():
    return data()


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
def test_calculates_total_uncertainty(dataset):
    with open_loggs() as loggs:
        tot = TotalUncertainty(TotalUncertaintyOptions(particle="#pi^{0}"))
        Comparator().compare(tot.transform(dataset, loggs))
