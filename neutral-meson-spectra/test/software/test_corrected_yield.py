import unittest

# from spectrum.spectrum import Spectrum
from spectrum.corrected_yield import CorrectedYield
from spectrum.options import CorrectedYieldOptions
from spectrum.options import CompositeCorrectedYieldOptions
from spectrum.output import AnalysisOutput

from vault.datavault import DataVault


class TestCorrectedYield(unittest.TestCase):

    def test_interface_simple(self):
        data = [
            DataVault().input("data"),
            DataVault().input("pythia8")
        ]

        estimator = CorrectedYield(
            CorrectedYieldOptions(particle="#pi^{0}"),
            plot=False
        )
        cyield = estimator.transform(
            data,
            loggs=AnalysisOutput("test simple corr. yield interface")
        )
        self.assertGreater(cyield.GetEntries(), 0)

    def test_interface_composite(self):
        unified_inputs = {
            DataVault().input("single #pi^{0}", "low"): (0, 7.0),
            DataVault().input("single #pi^{0}", "high"): (7.0, 20)
        }

        data = [
            DataVault().input("data"),
            unified_inputs
        ]

        estimator = CorrectedYield(
            CompositeCorrectedYieldOptions(
                particle="#pi^{0}",
                unified_inputs=unified_inputs
            ),
            plot=False
        )
        cyield = estimator.transform(
            data,
            loggs=AnalysisOutput("test composite corr. yield interface")
        )
        self.assertGreater(cyield.GetEntries(), 0)
