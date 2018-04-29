import unittest
from vault.datavault import DataVault
from tools.ep import EpRatioEstimator
from spectrum.options import EpRatioOptions
from spectrum.comparator import Comparator


class TestEpRatio(unittest.TestCase):
    def test_ep_ratio(self):
        estimator = EpRatioEstimator(EpRatioOptions())
        output = estimator.transform(
            DataVault().input("pythia8", "epratio", listname='EpRatioTender'),
            "test ep ratio estimator"
        )
        Comparator().compare(output)
