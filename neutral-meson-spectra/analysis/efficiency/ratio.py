import pytest

from spectrum.pipeline import ComparePipeline
from spectrum.efficiency import Efficiency
from spectrum.options import CompositeEfficiencyOptions
from spectrum.output import AnalysisOutput

from vault.datavault import DataVault


@pytest.fixture
def data():
    eta_data = (
        DataVault().input("single #eta", "low", "PhysEff"),
        DataVault().input("single #eta", "high", "PhysEff"),
    )
    pion_data = (
        DataVault().input("single #pi^{0}", "low", "PhysEff"),
        DataVault().input("single #pi^{0}", "high", "PhysEff"),
    )
    return eta_data, pion_data


@pytest.mark.interactive
@pytest.mark.onlylocal
def test_efficiency_ratio(data):
    ptrange = "config/pt-same.json"
    opt_eta = CompositeEfficiencyOptions("#eta", ptrange=ptrange)
    opt_pi0 = CompositeEfficiencyOptions("#pi^{0}", ptrange=ptrange)
    estimator = ComparePipeline([
        ("#eta", Efficiency(opt_eta)),
        ("#pi^{0}", Efficiency(opt_pi0)),
    ])
    loggs = AnalysisOutput("efficiency_ratio")
    estimator.transform(data, loggs)
    loggs.plot()
