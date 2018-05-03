import unittest

from tools.probe import TagAndProbe
from vault.datavault import DataVault
from spectrum.options import ProbeTofOptions
from spectrum.output import AnalysisOutput


class TestProbe(unittest.TestCase):

    def test_interface(self):
        probe = TagAndProbe(ProbeTofOptions())
        eff = probe.transform(
            [
                DataVault().input(
                    "data",
                    "uncorrected",
                    "TagAndProbleTOFOnlyTender",
                    histname="MassEnergyTOF_SM0"),
                DataVault().input(
                    "data",
                    "uncorrected",
                    "TagAndProbleTOFOnlyTender",
                    histname="MassEnergyAll_SM0"),
            ],
            loggs=AnalysisOutput("Test the tag and probe interface")
        )
        self.assertGreater(eff.GetEntries(), 0)
