import unittest
import pytest

from spectrum.corrected_yield import CorrectedYield
from spectrum.options import CorrectedYieldOptions
from spectrum.options import CompositeCorrectedYieldOptions
from spectrum.output import AnalysisOutput
from tools.feeddown import data_feeddown

from vault.datavault import DataVault


class TestCorrectedPionYield(unittest.TestCase):

    def setUp(self):
        self.particle = "#pi^{0}"
        self.data_feeddown = data_feeddown()

    @pytest.mark.onlylocal
    def test_interface_simple(self):
        data = (
            (
                DataVault().input("data"),
                self.data_feeddown,
            ),
            DataVault().input("pythia8")
        )

        estimator = CorrectedYield(
            CorrectedYieldOptions(particle=self.particle),
            plot=False
        )
        cyield = estimator.transform(
            data,
            loggs=AnalysisOutput("test simple corr. yield interface")
        )
        self.assertGreater(cyield.GetEntries(), 0)

    @pytest.mark.onlylocal
    def test_interface_composite(self):
        data = (
            (
                DataVault().input("data"),
                self.data_feeddown,
            ),
            (
                DataVault().input("single #pi^{0}", "low"),
                DataVault().input("single #pi^{0}", "high"),
            )
        )

        estimator = CorrectedYield(
            CompositeCorrectedYieldOptions(particle=self.particle),
            plot=False
        )
        cyield = estimator.transform(
            data,
            loggs=AnalysisOutput("test composite corr. yield interface")
        )
        self.assertGreater(cyield.GetEntries(), 0)


class TestCorrectedEtaYield(TestCorrectedPionYield):

    def setUp(self):
        self.particle = "#eta"
        self.data_feeddown = None
