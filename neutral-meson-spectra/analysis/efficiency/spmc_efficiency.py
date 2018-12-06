import unittest

# from spectrum.comparator import Comparator
from spectrum.efficiency import Efficiency
from spectrum.options import CompositeEfficiencyOptions
from spectrum.output import AnalysisOutput
from spectrum.broot import BROOT as br
from spectrum.comparator import Comparator

from tools.validate import validate
from vault.datavault import DataVault

PION_INPUT = (
    DataVault().input("single #pi^{0}", "low", "PhysEff"),
    DataVault().input("single #pi^{0}", "high", "PhysEff"),
)

ETA_INPUT = (
    DataVault().input("single #eta", "low"),
    DataVault().input("single #eta", "high"),
)


class TestEfficiencyPi0(unittest.TestCase):

    @unittest.skip("TODO: Update me")
    def test_pi0_efficiency(self):
        efficiency = evaluate_spmc_efficiency(PION_INPUT, "#pi^{0}")
        validate(self, br.hist2dict(efficiency), "spmc_efficiency/#pi^{0}")


# @unittest.skip("")
# @pytest.mark.skip("")
def test_eta_efficiency():
    evaluate_spmc_efficiency(ETA_INPUT, "#eta")


def evaluate_spmc_efficiency(inputs, particle):
    options = CompositeEfficiencyOptions(particle)
    loggs = AnalysisOutput("efficiency_spmc_{}".format(particle))
    efficiency = Efficiency(options).transform(
        inputs,
        loggs
    )
    # diff = Comparator()
    # diff.compare(efficiency)
    loggs.plot()
    return efficiency
