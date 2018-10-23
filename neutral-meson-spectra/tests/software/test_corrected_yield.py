import unittest
import pytest

from spectrum.corrected_yield import CorrectedYield
from spectrum.options import CorrectedYieldOptions
from spectrum.options import CompositeCorrectedYieldOptions
from spectrum.output import AnalysisOutput
from tools.feeddown import data_feeddown

from vault.datavault import DataVault


class TestCorrectedYield(unittest.TestCase):

    @pytest.mark.onlylocal
    def test_interface_simple(self):
        data = (
            (
                DataVault().input("data"),
                data_feeddown(),
            ),
            DataVault().input("pythia8")
        )

        estimator = CorrectedYield(
            CorrectedYieldOptions(particle="#pi^{0}"),
            plot=False
        )
        cyield = estimator.transform(
            data,
            loggs=AnalysisOutput("test simple corr. yield interface")
        )
        self.assertGreater(cyield.GetEntries(), 0)

    @unittest.skip("Fix this test later")
    def test_interface_composite(self):
        data = (
            (
                DataVault().input("data"),
                data_feeddown(),
            ),
            (
                DataVault().input("single #pi^{0}", "low"),
                DataVault().input("single #pi^{0}", "high"),
            )
        )

        estimator = CorrectedYield(
            CompositeCorrectedYieldOptions(particle="#pi^{0}"),
            plot=False
        )
        cyield = estimator.transform(
            data,
            loggs=AnalysisOutput("test composite corr. yield interface")
        )
        self.assertGreater(cyield.GetEntries(), 0)
