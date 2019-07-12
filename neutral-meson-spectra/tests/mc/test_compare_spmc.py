import pytest
from spectrum.pipeline import ComparePipeline
from spectrum.efficiency import Efficiency
from spectrum.options import EfficiencyOptions
from spectrum.options import CompositeEfficiencyOptions
from spectrum.output import open_loggs
from vault.datavault import DataVault


@pytest.fixture
def spmc():
    return (
        DataVault().input("single #pi^{0}", "low", "PhysEff"),
        DataVault().input("single #pi^{0}", "high", "PhysEff"),
    )


@pytest.fixture
def pythia8():
    return DataVault().input("pythia8")


@pytest.fixture
def data(spmc, pythia8):
    return spmc, pythia8


@pytest.mark.onlylocal
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    # "#eta",
])
def test_efficiencies(particle, data):
    general_options = EfficiencyOptions(
        genname="hPt_#pi^{0}_primary_",
        scale=2,
        pt="config/pt-same-truncated.json"
    )

    steps = [
        ("spmc", Efficiency(CompositeEfficiencyOptions(particle)))
        ("pythia8", Efficiency(general_options))
    ]

    with open_loggs("pythia8 spmc ratio") as loggs:
        estimator = ComparePipeline(steps, plot=False)
        estimator.transform(data, loggs)
