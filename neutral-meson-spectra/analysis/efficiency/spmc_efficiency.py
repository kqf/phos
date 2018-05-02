import unittest

from spectrum.comparator import Comparator

from spectrum.efficiency import Efficiency
from spectrum.options import MultirangeEfficiencyOptions

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

    @unittest.skip('')
    def test_pi0_efficiency(self):
        unified_inputs = {
            DataVault().input(
                "single #pi^{0} iteration3 yield aliphysics",
                "low"
            ): (0, 7.0),
            DataVault().input(
                "single #pi^{0} iteration3 yield aliphysics",
                "high"
            ): (7.0, 20)
        }
        evaluate_spmc_efficiency(unified_inputs, "#pi^{0}")


class TestEfficiencyEta(unittest.TestCase):

    # @unittest.skip('')
    def test_eta_efficiency(self):
        unified_inputs = {
            DataVault().input("single #eta new tender", "low"): (0, 6),
            DataVault().input("single #eta new tender", "high"): (6, 20)
        }
        evaluate_spmc_efficiency(unified_inputs, "#eta")


def evaluate_spmc_efficiency(unified_inputs, particle):
    options = MultirangeEfficiencyOptions.spmc(
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

    efficiency.SetTitle(
        "#varepsilon = #Delta #phi #Delta y/ 2 #pi "
        "#frac{Number of reconstructed %s}{Number of generated primary %s}"
        % (particle, particle)
    )

    diff = Comparator()
    diff.compare(efficiency)
