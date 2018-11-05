import unittest

# from spectrum.comparator import Comparator
from spectrum.efficiency import Efficiency
from spectrum.options import CompositeEfficiencyOptions
from spectrum.output import AnalysisOutput
from spectrum.broot import BROOT as br

from tools.validate import validate
from vault.datavault import DataVault


class TestFakeEfficiencyPi0(unittest.TestCase):

    @unittest.skip('')
    def test_artificial_efficiency(self):
        inputs = {
            "LHC16-single-low.root": (0.0, 8.0),
            "LHC16-single.root": (4.0, 20.0)
        }
        evaluate_spmc_efficiency(inputs, "#pi^{0}")


class TestEfficiencyPi0(unittest.TestCase):

    # @unittest.skip('')
    def test_pi0_efficiency(self):
        production = "single #pi^{0}"
        inputs = (
            DataVault().input(production, "low", "PhysEff"),
            DataVault().input(production, "high", "PhysEff"),
        )
        efficiency = evaluate_spmc_efficiency(inputs, "#pi^{0}")
        validate(self, br.hist2dict(efficiency), "spmc_efficiency/#pi^{0}")


class TestEfficiencyEta(unittest.TestCase):

    @unittest.skip('')
    def test_eta_efficiency(self):
        # production = "single #eta updated nonlinearity"
        production = "single #eta new tender"
        inputs = [
            DataVault().input(production, "low"),
            DataVault().input(production, "high"),
        ]
        evaluate_spmc_efficiency(inputs, "#eta")


def evaluate_spmc_efficiency(inputs, particle):
    options = CompositeEfficiencyOptions(particle)
    loggs = AnalysisOutput("composite_efficiency_spmc_{}".format(particle))
    efficiency = Efficiency(options).transform(
        inputs,
        loggs
    )
    # diff = Comparator()
    # diff.compare(efficiency)
    # loggs.plot()
    return efficiency
