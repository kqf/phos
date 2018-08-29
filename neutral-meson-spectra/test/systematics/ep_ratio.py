import unittest
from vault.datavault import DataVault
from tools.ep import EpRatioEstimator
from spectrum.options import EpRatioOptions
from spectrum.comparator import Comparator


class TestEpRatio(unittest.TestCase):
    def test_ep_ratio(self):
        estimator = EpRatioEstimator(EpRatioOptions())
        output = estimator.transform(
            DataVault().input("pythia8", version="ep_ratio", listname="EpRatio"),
            "test ep ratio estimator"
        )
        for o in output:
	        Comparator().compare(o)
