import unittest
import ROOT

from spectrum.input import Input
from spectrum.output import AnalysisOutput
from spectrum.comparator import Comparator
from spectrum.broot import BROOT as br

from spectrum.efficiency import Efficiency, EfficiencyMultirange
from spectrum.options import EfficiencyOptions, MultirangeEfficiencyOptions

from vault.datavault import DataVault


class TestEfficiencyPi0(unittest.TestCase):

    def test_pi0_efficiency(self):
        unified_inputs = {
            DataVault().file("single #pi^{0}", "low"): (0, 7),
            DataVault().file("single #pi^{0}", "high"): (7, 20)
        }
        evaluate_spmc_efficiency(unified_inputs, "#pi^{0}")


class TestEfficiencyEta(unittest.TestCase):

    @unittest.skip('')
    def test_pi0_efficiency(self):
        unified_inputs = {
            DataVault().file("single #eta", "low"): (0, 6),
            DataVault().file("single #eta", "high"): (6, 20)
        }
        evaluate_spmc_efficiency(unified_inputs, "#eta")


def evaluate_spmc_efficiency(unified_inputs, particle):

    estimator = EfficiencyMultirange(
       MultirangeEfficiencyOptions.spmc(unified_inputs, particle)
    )

    loggs = AnalysisOutput("composite_efficiency_spmc_{}".format(particle), particle)

    efficiency = estimator.transform(
       [Input(filename, "PhysEff") for filename in unified_inputs],
       loggs
    )

    efficiency.SetTitle(
        "#varepsilon = #Delta #phi #Delta y/ 2 #pi " \
        "#frac{Number of reconstructed %s}{Number of generated primary %s}" \
        % (particle, particle)
    )
    diff = Comparator()
    diff.compare(efficiency)
    loggs.plot(False)

