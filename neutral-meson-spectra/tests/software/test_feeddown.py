import pytest
import numpy as np

from spectrum.tools.feeddown import FeeddownEstimator, data_feeddown
from spectrum.options import FeeddownOptions
from spectrum.output import open_loggs
try:
    import root_numpy as rp
except ValueError:
    from spectrum.broot import BROOT as rp


@pytest.mark.onlylocal
def test_pion():
    estimator = FeeddownEstimator(FeeddownOptions(particle="#pi^{0}"))
    with open_loggs() as loggs:
        output = estimator.transform(data_feeddown(), loggs)
    assert output.GetEntries() > 0


@pytest.mark.onlylocal
def test_handles_non_pions_with_data():
    estimator = FeeddownEstimator(FeeddownOptions(particle="#eta"))
    with pytest.raises(IOError):
        with open_loggs() as loggs:
            estimator.transform(data_feeddown(), loggs)


@pytest.mark.onlylocal
def test_eta():
    estimator = FeeddownEstimator(FeeddownOptions(particle="#eta"))
    with open_loggs() as loggs:
        output = estimator.transform(None, loggs)

    answer = rp.hist2array(output)
    assert np.all(answer == np.ones_like(answer))
