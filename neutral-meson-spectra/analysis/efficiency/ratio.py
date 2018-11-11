import unittest

from spectrum.pipeline import ComparePipeline
from spectrum.efficiency import Efficiency
from spectrum.options import CompositeEfficiencyOptions
from spectrum.output import AnalysisOutput

from vault.datavault import DataVault


class TestFakeEfficiencyPi0(unittest.TestCase):

    def test_efficiency_ratio(self):
        eta_inputs = (
            DataVault().input("single #eta", "low", "PhysEff"),
            DataVault().input("single #eta", "high", "PhysEff"),
        )
        pi0_inputs = (
            DataVault().input("single #pi^{0}", "low", "PhysEff"),
            DataVault().input("single #pi^{0}", "high", "PhysEff"),
        )
        opt_eta = CompositeEfficiencyOptions("#eta", ptrange="config/pt.json")
        opt_pi0 = CompositeEfficiencyOptions("#pi^{0}",
                                             ptrange="config/pt.json")
        estimator = ComparePipeline([
            ("#eta", Efficiency(opt_eta)),
            ("#pi^{0}", Efficiency(opt_pi0)),
        ])
        loggs = AnalysisOutput("efficiency_ratio")
        estimator.transform((eta_inputs, pi0_inputs), loggs)
        loggs.plot()
