import pytest

from spectrum.efficiency import Efficiency
from spectrum.pipeline import ComparePipeline
from spectrum.options import EfficiencyOptions
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
    return (
        DataVault().input("single #pi^{0}", listname="PhysEff"),
        DataVault().input("single #pi^{0}", listname="PhysEff")
    )


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
    spmc_ratio = efficiency_ratio(spmc, "spmc")
    pythia_ratio = efficiency_ratio(pythia, "pythia")
    Comparator().compare(spmc_ratio, pythia_ratio)
