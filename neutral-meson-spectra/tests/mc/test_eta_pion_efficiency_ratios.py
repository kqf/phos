import pytest

from spectrum.efficiency import Efficiency
from spectrum.pipeline import ComparePipeline
from spectrum.options import EfficiencyOptions, CompositeEfficiencyOptions
from spectrum.output import open_loggs

from vault.datavault import DataVault
from spectrum.comparator import Comparator


@pytest.fixture
def pythia():
    return (
        DataVault().input("pythia8", "fake", listname="PhysEff"),
        DataVault().input("pythia8", "fake", listname="PhysEff")
    )


@pytest.fixture
def spmc():
    eta = (
        DataVault().input("single #eta", "low", listname="PhysEff"),
        DataVault().input("single #eta", "high", listname="PhysEff")
    )
    pion = (
        DataVault().input("single #pi^{0}", "low", listname="PhysEff"),
        DataVault().input("single #pi^{0}", "high", listname="PhysEff")
    )
    return eta, pion


# @pytest.mark.skip("")
@pytest.mark.onlylocal
@pytest.mark.interactive
def test_efficiency_ratio(pythia, spmc):
    pt = "config/pt-same.json"
    estimator = ComparePipeline([
        ("#eta", Efficiency(
            EfficiencyOptions(particle="#eta", pt=pt, scale=1))),
        ("#pi^{0}", Efficiency(
            EfficiencyOptions(particle="#pi^{0}", pt=pt, scale=1))),
    ], plot=True)

    with open_loggs() as loggs:
        pythia_ratio = estimator.transform(pythia, loggs)

    # Now the similar code for SPMC
    estimator = ComparePipeline([
        ("#eta", Efficiency(
            CompositeEfficiencyOptions(particle="#eta", pt=pt, scale=1))),
        ("#pi^{0}", Efficiency(
            CompositeEfficiencyOptions(particle="#pi^{0}", pt=pt, scale=1))),
    ], plot=True)
    with open_loggs() as loggs:
        spmc_ratio = estimator.transform(spmc, loggs)

    Comparator(labels=["spmc", "pythia"]).compare(spmc_ratio, pythia_ratio)


@pytest.mark.skip("")
@pytest.mark.onlylocal
@pytest.mark.interactive
def test_spmc_efficiency(pythia, spmc):
    pt = "config/pt-same.json"

    # Now the similar code for SPMC
    estimator = ComparePipeline([
        ("#eta", Efficiency(
            CompositeEfficiencyOptions(particle="#eta", pt=pt,
                                       scale=1))),
        ("#pi^{0}", Efficiency(
            CompositeEfficiencyOptions(particle="#pi^{0}", pt=pt,
                                       scale=1))),
    ], plot=True)
    with open_loggs() as loggs:
        estimator.transform(spmc, loggs)


@pytest.mark.skip("")
@pytest.mark.onlylocal
@pytest.mark.interactive
def test_pion_efficiency(pythia, spmc):
    pt = "config/pt-same.json"

    estimator = Efficiency(
        EfficiencyOptions(particle="#eta", pt=pt, scale=1))

    with open_loggs("test eta pythia efficiency") as loggs:
        estimator.transform(pythia[1], loggs)
