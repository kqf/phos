import pytest

from lazy_object_proxy import Proxy
from spectrum.pipeline import ComparePipeline
from spectrum.efficiency import Efficiency
from spectrum.options import CompositeEfficiencyOptions
from spectrum.output import AnalysisOutput

from vault.datavault import DataVault

ETA_INPUTS = Proxy(
    lambda: (
        DataVault().input("single #eta", "low", "PhysEff"),
        DataVault().input("single #eta", "high", "PhysEff"),
    )
)

PI0_INPUTS = Proxy(
    lambda: (
        DataVault().input("single #pi^{0}", "low", "PhysEff"),
        DataVault().input("single #pi^{0}", "high", "PhysEff"),
    )
)


@pytest.mark.onlylocal
def test_efficiency_ratio(self):
    ptrange = "config/pt-same.json"
    opt_eta = CompositeEfficiencyOptions("#eta", ptrange=ptrange)
    opt_pi0 = CompositeEfficiencyOptions("#pi^{0}", ptrange=ptrange)
    estimator = ComparePipeline([
        ("#eta", Efficiency(opt_eta)),
        ("#pi^{0}", Efficiency(opt_pi0)),
    ])
    loggs = AnalysisOutput("efficiency_ratio")
    estimator.transform((ETA_INPUTS, PI0_INPUTS), loggs)
    loggs.plot()
