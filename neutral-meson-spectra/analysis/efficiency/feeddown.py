import pytest
from spectrum.tools.feeddown import FeeddownEstimator, data_feeddown

from spectrum.options import FeeddownOptions
from spectrum.output import open_loggs
from spectrum.comparator import Comparator


@pytest.mark.onlylocal
@pytest.mark.interactive
def test_feeddown_correction():
    options = FeeddownOptions()
    estimator = FeeddownEstimator(options)
    with open_loggs("feeddown correction") as loggs:
        output = estimator.transform(data_feeddown(), loggs)
        Comparator().compare(output)
    assert output.GetEntries() > 0
