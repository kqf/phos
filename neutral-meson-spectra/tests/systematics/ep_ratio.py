import unittest
from tools.ep import EpRatioEstimator

from vault.datavault import DataVault
from spectrum.options import EpRatioOptions
from spectrum.comparator import Comparator
# from spectrum.output import AnalysisOutput


class EpRatio(unittest.TestCase):

    # @unittest.skip("")
    def test_ep_ratio(self):
        options = EpRatioOptions()
        options.histname = "hEp_ele"
        estimator = EpRatioEstimator(options, plot=True)
        output = estimator.transform(
            DataVault().input(
                "pythia8",
                version="ep_ratio_1",
                listname="PHOSEpRatioCoutput1",
                histname="Ep_ele",
                use_mixing=False),
            loggs="test ep ratio estimator"
        )

        for o in output:
            Comparator().compare(o)
