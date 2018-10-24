import unittest
import pytest
import numpy as np
import root_numpy as rnp

from tools.feeddown import FeeddownEstimator, data_feeddown
from spectrum.options import FeeddownOptions
from spectrum.output import AnalysisOutput


class FeddownTestInterface(unittest.TestCase):
    @pytest.mark.onlylocal
    def test_pion(self):
        estimator = FeeddownEstimator(FeeddownOptions())
        output = estimator.transform(
            data_feeddown(),
            AnalysisOutput("feeddown correction")
        )
        self.assertGreater(output.GetEntries(), 0)

    def test_handles_non_pions_with_data(self):
        estimator = FeeddownEstimator(FeeddownOptions(particle="#eta"))
        self.assertRaises(IOError, estimator.transform, data_feeddown(), "")

    def test_(self):
        estimator = FeeddownEstimator(FeeddownOptions(particle="#eta"))
        output = estimator.transform(
            None,
            AnalysisOutput("feeddown correction")
        )
        answer = rnp.hist2array(output)
        self.assertTrue(np.all(answer == np.ones_like(answer)))
