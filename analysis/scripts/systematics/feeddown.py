import pytest

from spectrum.output import open_loggs
from spectrum.comparator import Comparator  # noqa

from spectrum.uncertainties.feeddown import FeedDown
from spectrum.uncertainties.feeddown import FeedDownOptions
from spectrum.uncertainties.feeddown import feeddown_data


@pytest.fixture
def data():
    return feeddown_data()


@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.interactive
def test_feeddown(data, stop):
    tof = FeedDown(FeedDownOptions(particle="#pi^{0}"))
    with open_loggs() as loggs:
        output = tof.transform(data, loggs)
        Comparator(stop=stop).compare(output)
    assert len(output) > 0
