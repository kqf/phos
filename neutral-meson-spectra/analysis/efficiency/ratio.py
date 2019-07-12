import pytest

from spectrum.pipeline import ComparePipeline
from spectrum.efficiency import Efficiency
from spectrum.options import CompositeEfficiencyOptions
from spectrum.output import open_loggs

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
    pt = "config/pt-same.json"
    opt_eta = CompositeEfficiencyOptions("#eta", pt=pt)
    opt_pi0 = CompositeEfficiencyOptions("#pi^{0}", pt=pt)
    estimator = ComparePipeline([
        ("#eta", Efficiency(opt_eta)),
        ("#pi^{0}", Efficiency(opt_pi0)),
    ])
    with open_loggs("efficiency_ratio") as loggs:
        estimator.transform(data, loggs)
