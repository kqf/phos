import unittest

from spectrum.options import CompositeCorrectedYieldOptions
from spectrum.output import AnalysisOutput
from vault.datavault import DataVault
from uncertainties.yields import YieldExtractioin
from spectrum.comparator import Comparator


class YieldExtractioinUncertanityOptions(object):
    def __init__(self, cyield):
        self.mass_range = {
            "low": [0.06, 0.22],
            # "mid": [0.04, 0.20],
            # "wide": [0.08, 0.24]
        }
        self.backgrounds = ["pol1"]
        self.signals = ["CrystalBall"]
        self.nsigmas = [2]
        self.cyield = cyield


class TestYieldExtractionUncertanity(unittest.TestCase):

    # @unittest.skip("")
    def test_yield_extraction_uncertanity_pion(self):
        production = "single #pi^{0} iteration d3 nonlin14"
        inputs = (
            DataVault().input(production, "low"),
            DataVault().input(production, "high"),
        )

        data = [
            DataVault().input("data"),
            inputs
        ]

        options = YieldExtractioinUncertanityOptions(
            CompositeCorrectedYieldOptions(particle="#pi^{0}")
        )
        estimator = YieldExtractioin(options)
        output = estimator.transform(
            data,
            loggs=AnalysisOutput("corrected yield #pi^{0}")
        )
        Comparator().compare(output)
