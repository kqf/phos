import pytest

from spectrum.efficiency import Efficiency
from spectrum.pipeline import ComparePipeline
from spectrum.options import EfficiencyOptions, CompositeEfficiencyOptions
from spectrum.output import AnalysisOutput

from vault.datavault import DataVault
from spectrum.comparator import Comparator


@pytest.fixture
def pythia():
    return (
        DataVault().input("pythia8", listname="PhysEff"),
        DataVault().input("pythia8", listname="PhysEff")
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
    return (eta, pion)


def efficiency_ratio(data, name):
    ptrange = "config/pt-same.json"
    estimator = ComparePipeline([
        ("#eta", Efficiency(
            EfficiencyOptions(particle="#eta", ptrange=ptrange, scale=1))),
        ("#pi^{0}", Efficiency(
            EfficiencyOptions(particle="#pi^{0}", ptrange=ptrange, scale=1))),
    ], plot=True)
    loggs = AnalysisOutput("efficiency_ratio_{}".format(name))
    output = estimator.transform(data, loggs)
    loggs.plot()
    return output


# @pytest.mark.skip("")
@pytest.mark.onlylocal
@pytest.mark.interactive
def test_efficiency(pythia, spmc):
    ptrange = "config/pt-same.json"
    estimator = ComparePipeline([
        ("#eta", Efficiency(
            EfficiencyOptions(particle="#eta", ptrange=ptrange, scale=1))),
        ("#pi^{0}", Efficiency(
            EfficiencyOptions(particle="#pi^{0}", ptrange=ptrange, scale=1))),
    ], plot=True)

    loggs = AnalysisOutput("efficiency_ratio_spmc")
    pythia_ratio = estimator.transform(pythia, loggs)
    # loggs.plot()

    # Now the similar code for SPMC
    estimator = ComparePipeline([
        ("#eta", Efficiency(
            CompositeEfficiencyOptions(particle="#eta", ptrange=ptrange,
                                       scale=1))),
        ("#pi^{0}", Efficiency(
            CompositeEfficiencyOptions(particle="#pi^{0}", ptrange=ptrange,
                                       scale=1))),
    ], plot=True)
    loggs = AnalysisOutput("efficiency_ratio_spmc")
    spmc_ratio = estimator.transform(spmc, loggs)
    # loggs.plot()
    Comparator(labels=["spmc", "pythia"]).compare(spmc_ratio, pythia_ratio)
