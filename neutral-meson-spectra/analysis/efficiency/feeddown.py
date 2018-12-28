from tools.feeddown import FeeddownEstimator, data_feeddown

from spectrum.options import FeeddownOptions
from spectrum.output import AnalysisOutput
from spectrum.comparator import Comparator


def test_feeddown_correction():
    options = FeeddownOptions()
    estimator = FeeddownEstimator(options)
    loggs = AnalysisOutput("feeddown correction")
    output = estimator.transform(data_feeddown(), loggs)
    # loggs.plot()
    print "first bin", output.GetBinContent(1)
    Comparator().compare([output])
    assert output.GetEntries() > 0
