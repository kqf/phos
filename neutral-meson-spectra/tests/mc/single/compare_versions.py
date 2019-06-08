import pytest

from spectrum.pipeline import ComparePipeline
from spectrum.efficiency import Efficiency
from spectrum.options import CompositeEfficiencyOptions
from spectrum.options import CompositeOptions
from spectrum.analysis import Analysis
from spectrum.output import open_loggs

from vault.datavault import DataVault


@pytest.fixture
def data():
    datasets = [
        (
            DataVault().input("single #pi^{0}", "low", listname="PhysEff" + i),
            DataVault().input("single #pi^{0}", "high", listname="PhysEff" + i)
        )
        for i in ["", "1", "3"]
    ]

    names = "old", "new", "the oldest one"
    return names, datasets


@pytest.mark.onlylocal
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    # "#eta",
])
def test_efficiencies(data, particle):
    names, datasets = data
    estimator = ComparePipeline([
        (name, Efficiency(CompositeEfficiencyOptions(
            uinput,
            particle,
        )))
        for name, uinput in zip(names, datasets)
    ], plot=True)

    with open_loggs("compare different productions") as loggs:
        estimator.transform(datasets, loggs)


@pytest.mark.onlylocal
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    # "#eta",
])
def test_yields(data, particle):
    names, datasets = data
    estimator = ComparePipeline([
        (name, Analysis(CompositeOptions(uinput, particle)))
        for name, uinput in zip(names, datasets)
    ], True)

    with open_loggs("compare yields") as loggs:
        estimator.transform(datasets, loggs)
