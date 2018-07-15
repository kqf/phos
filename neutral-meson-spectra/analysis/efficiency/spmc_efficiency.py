import unittest

from spectrum.comparator import Comparator

from spectrum.efficiency import Efficiency
from spectrum.options import CompositeEfficiencyOptions
from spectrum.output import AnalysisOutput

from vault.datavault import DataVault


class TestFakeEfficiencyPi0(unittest.TestCase):

    @unittest.skip('')
    def test_artificial_efficiency(self):
        unified_inputs = {
            "LHC16-single-low.root": (0.0, 8.0),
            "LHC16-single.root": (4.0, 20.0)
        }
        evaluate_spmc_efficiency(unified_inputs, "#pi^{0}")


class TestEfficiencyPi0(unittest.TestCase):

    # @unittest.skip('')
    def test_pi0_efficiency(self):
        # production = "single #pi^{0} iteration3 yield aliphysics"
        # production = "single #pi^{0} iteration d3 nonlin14"
        production = "single #pi^{0} debug7"
        unified_inputs = {
            DataVault().input(production, "low", "PhysEff"): (0.0, 7.0),
            # DataVault().input(production, "high", "PhysEff"): (4.0, 20.0),
            DataVault().input(production, "high", "PhysEff"): (5.0, 20.0),
        }
        evaluate_spmc_efficiency(unified_inputs, "#pi^{0}")


class TestEfficiencyEta(unittest.TestCase):

    @unittest.skip('')
    def test_eta_efficiency(self):
        production = "single #eta nonlin"
        # production = "single #eta new tender"
        unified_inputs = {
            DataVault().input(production, "low"): (0.0, 10.0),
            DataVault().input(production, "high"): (4.0, 20.0)
        }
        evaluate_spmc_efficiency(unified_inputs, "#eta")


def evaluate_spmc_efficiency(unified_inputs, particle):
    options = CompositeEfficiencyOptions(unified_inputs, particle)
    # for options in options.suboptions:
    # options.analysis.signalp.relaxed = True
    # options.analysis.backgroundp.relaxed = True

    loggs = AnalysisOutput("composite_efficiency_spmc_{}".format(particle))
    efficiency = Efficiency(options).transform(
        unified_inputs,
        loggs
    )
    diff = Comparator()
    diff.compare(efficiency)
    loggs.plot()
