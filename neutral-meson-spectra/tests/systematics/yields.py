import unittest

from spectrum.options import CompositeCorrectedYieldOptions
from spectrum.output import AnalysisOutput
from vault.datavault import DataVault
from uncertainties.yields import YieldExtractioin
from uncertainties.yields import YieldExtractioinUncertanityOptions
from spectrum.comparator import Comparator


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
