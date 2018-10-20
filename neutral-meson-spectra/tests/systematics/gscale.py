import unittest
from vault.datavault import DataVault
from spectrum.options import CompositeCorrectedYieldOptions
from spectrum.output import AnalysisOutput
from uncertainties.gscale import GScale
from spectrum.comparator import Comparator


class TestGeScaleUncertainty(unittest.TestCase):
    def test_interface_composite(self):
        estimator = GScale(
            CompositeCorrectedYieldOptions(particle="#pi^{0}"),
            plot=False
        )
        uncertanity = estimator.transform(
            (
                (
                    DataVault().input("data"),
                    (
                        DataVault().input("single #pi^{0}", "low"),
                        DataVault().input("single #pi^{0}", "high"),
                    )
                ),
                (
                    DataVault().input("data"),
                    (
                        DataVault().input("single #pi^{0}", "low"),
                        DataVault().input("single #pi^{0}", "high"),
                    )
                ),
            ),
            loggs=AnalysisOutput("test composite corr. yield interface")
        )
        Comparator().compare(uncertanity)
        return uncertanity
