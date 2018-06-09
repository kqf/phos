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
        unified_inputs = {
            DataVault().input(production, "low", "PhysEff"): (0.0, 8.0),
            DataVault().input(production, "high", "PhysEff"): (4.0, 20.0),
        }

        estimator = PeakPositionWidthEstimator(
            CompositeEfficiencyOptions(unified_inputs, "#pi^{0}")
        )
        loggs = AnalysisOutput("test ranges")
        mass, massf, width, widthf = estimator._estimate(
            unified_inputs,
            loggs
        )
        # loggs.plot()
        Comparator().compare(mass)
        Comparator().compare(width)
        print br.pars(widthf)
