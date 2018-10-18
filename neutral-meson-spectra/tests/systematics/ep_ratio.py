import unittest
from tools.ep import EpRatioEstimator, DataMCEpRatioEstimator

from vault.datavault import DataVault
from spectrum.options import EpRatioOptions, DataMCEpRatioOptions
from spectrum.comparator import Comparator
# from spectrum.output import AnalysisOutput


def data(prod="data", version="ep_ratio"):
    return DataVault().input(
        prod,
        version=version,
        listname="PHOSEpRatioCoutput1",
        histname="Ep_ele",
        use_mixing=False)


class EpRatio(unittest.TestCase):

    @unittest.skip("")
    def test_ep_ratio_mc(self):
        options = EpRatioOptions()
        estimator = EpRatioEstimator(options, plot=True)
        output = estimator.transform(
            data("pythia8", "ep_ratio_1"),
            loggs="test ep ratio estimator"
        )

        for o in output:
            Comparator().compare(o)

    @unittest.skip("")
    def test_ep_ratio_data(self):
        options = EpRatioOptions()
        estimator = EpRatioEstimator(options, plot=True)
        output = estimator.transform(
            data("data"),
            loggs="test ep ratio estimator"
        )

        for o in output:
            Comparator().compare(o)

    def test_data_mc_ratio(self):
        estimator = DataMCEpRatioEstimator(
            DataMCEpRatioOptions(), plot=False
        )
        output = estimator.transform(
            (
                data("data"),
                data("pythia8", "ep_ratio_1"),
            ),
            loggs="test double ep ratio estimator"
        )
        for o in output:
            Comparator().compare(o)
