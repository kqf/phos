import pytest
import numpy as np

from tools.feeddown import FeeddownEstimator, data_feeddown
from spectrum.options import FeeddownOptions
from spectrum.output import AnalysisOutput


@pytest.mark.onlylocal
def test_pion():
    estimator = FeeddownEstimator(FeeddownOptions())
    output = estimator.transform(
        data_feeddown(),
        AnalysisOutput("feeddown correction")
    )
    assert output.GetEntries() > 0


@pytest.mark.onlylocal
def test_handles_non_pions_with_data():
    estimator = FeeddownEstimator(FeeddownOptions(particle="#eta"))
    with pytest.raises(IOError):
        estimator.transform(data_feeddown(), "")


@pytest.mark.skip("fix root_numpy dependencies")
def test_eta():
    estimator = FeeddownEstimator(FeeddownOptions(particle="#eta"))
    output = estimator.transform(
        None,
        AnalysisOutput("feeddown correction")
    )
    import root_numpy as rnp
    answer = rnp.hist2array(output)
    assert np.all(answer == np.ones_like(answer))
