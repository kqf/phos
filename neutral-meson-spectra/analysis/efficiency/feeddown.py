import unittest

from tools.feeddown import FeeddownEstimator
from vault.datavault import DataVault

from spectrum.options import FeeddownOptions
from spectrum.output import AnalysisOutput
from spectrum.comparator import Comparator


class FeddownTest(unittest.TestCase):
    def test_feeddown_correction(self):
        options = FeeddownOptions()
        estimator = FeeddownEstimator(options)
        loggs = AnalysisOutput("feeddown correction")
        output = estimator.transform(
            [
                DataVault().input(
                    "pythia8",
                    listname="FeeddownSelection",
                    use_mixing=False,
                    histname="MassPt_#pi^{0}_feeddown_K^{s}_{0}",
                    prefix=""
                ),
                DataVault().input("pythia8", listname="FeeddownSelection"),
            ],
            loggs
        )
        # loggs.plot()
        Comparator().compare(output)
        self.assertGreater(output.GetEntries(), 0)
