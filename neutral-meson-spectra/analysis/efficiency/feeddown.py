import unittest

from tools.feeddown import FeeddownEstimator, data_feeddown

from spectrum.options import FeeddownOptions
from spectrum.output import AnalysisOutput
from spectrum.comparator import Comparator


class FeddownTest(unittest.TestCase):
    def test_feeddown_correction(self):
        options = FeeddownOptions()
        estimator = FeeddownEstimator(options)
        loggs = AnalysisOutput("feeddown correction")
        output = estimator.transform(data_feeddown(), loggs)
        # loggs.plot()
        print "first bin", output.GetBinContent(1)
        Comparator().compare([output])
        self.assertGreater(output.GetEntries(), 0)
