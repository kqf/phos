import unittest

from spectrum.comparator import Comparator

from spectrum.efficiency import Efficiency
from spectrum.options import CompositeEfficiencyOptions

from vault.datavault import DataVault


class TestFakeEfficiencyPi0(unittest.TestCase):

    @unittest.skip('')
    def test_artificial_efficiency(self):
        unified_inputs = {
            "LHC16-single-low.root": (0, 7),
            "LHC16-single.root": (7, 20)
        }
        evaluate_spmc_efficiency(unified_inputs, "#pi^{0}")


class TestEfficiencyPi0(unittest.TestCase):

    # @unittest.skip('')
    def test_pi0_efficiency(self):
        production = "single #pi^{0} iteration3 yield aliphysics"
        unified_inputs = {
            DataVault().input(production, "low"): (0, 7.0),
            DataVault().input(production, "high"): (7.0, 20)
        }
        evaluate_spmc_efficiency(unified_inputs, "#pi^{0}")


class TestEfficiencyEta(unittest.TestCase):

    @unittest.skip('')
    def test_eta_efficiency(self):
        production = "single #eta new tender"
        unified_inputs = {
            DataVault().input(production, "low"): (0, 6),
            DataVault().input(production, "high"): (6, 20)
        }
        evaluate_spmc_efficiency(unified_inputs, "#eta")


def evaluate_spmc_efficiency(unified_inputs, particle):
    options = CompositeEfficiencyOptions.spmc(
        unified_inputs,
        particle
    )
    # for options in options.suboptions:
    # options.analysis.signalp.relaxed = True
    # options.analysis.backgroundp.relaxed = True

    efficiency = Efficiency(options).transform(
        unified_inputs.keys(),
        "composite_efficiency_spmc_{}".format(particle)
    )

    diff = Comparator()
    diff.compare(efficiency)
