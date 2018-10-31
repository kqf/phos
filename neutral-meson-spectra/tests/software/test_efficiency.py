import unittest
import pytest

from spectrum.efficiency import Efficiency
from vault.datavault import DataVault
from spectrum.options import EfficiencyOptions, CompositeEfficiencyOptions
from spectrum.output import AnalysisOutput


class TestEfficiency(unittest.TestCase):

    def test_simple(self):
        estimator = Efficiency(
            EfficiencyOptions(genname='hPt_#pi^{0}_primary_'),
            plot=False
        )

        loggs = AnalysisOutput("test efficiency")
        efficiency = estimator.transform(
            DataVault().input("pythia8"),
            loggs=loggs
        )
        # loggs.plot()
        self.assertGreater(efficiency.GetEntries(), 0)

    @pytest.mark.onlylocal
    def test_composite(self):
        estimator = Efficiency(CompositeEfficiencyOptions("#pi^{0}"))
        loggs = AnalysisOutput("test composite efficiency")
        efficiency = estimator.transform(
            (
                DataVault().input("single #pi^{0}", "low"),
                DataVault().input("single #pi^{0}", "high"),
            ),
            loggs=loggs
        )
        # loggs.plot()
        self.assertGreater(efficiency.GetEntries(), 0)
