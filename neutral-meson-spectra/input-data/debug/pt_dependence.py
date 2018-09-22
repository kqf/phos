import unittest
from spectrum.options import CompositeEfficiencyOptions
from spectrum.output import AnalysisOutput
from spectrum.efficiency import PeakPositionWidthEstimator
from spectrum.comparator import Comparator
from spectrum.broot import BROOT as br
from vault.datavault import DataVault


class TestPeakPosition(unittest.TestCase):

    def test_pt_ranges(self):
        # production = "single #pi^{0} iteration3 yield aliphysics"
        production = "single #pi^{0} iteration d3 nonlin14"
        unified_inputs = (
            DataVault().input(production, "low", "PhysEff"),
            DataVault().input(production, "high", "PhysEff"),
        )

        estimator = PeakPositionWidthEstimator(
            CompositeEfficiencyOptions("#pi^{0}")
        )
        loggs = AnalysisOutput("test ranges")
        mass, massf, width, widthf = estimator._estimate(unified_inputs, loggs)
        # loggs.plot()
        Comparator().compare(mass)
        # Comparator().compare(width)
        print br.pars(massf)
