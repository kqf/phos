import pytest
from lazy_object_proxy import Proxy
from vault.datavault import DataVault
from spectrum.output import AnalysisOutput
from uncertainties.gscale import GScale, GScaleOptions
from spectrum.comparator import Comparator
from tools.feeddown import data_feeddown


def ep_data(prod="data", version="ep_ratio"):
    return DataVault().input(
        prod,
        version=version,
        listname="PHOSEpRatioCoutput1",
        histname="Ep_ele",
        use_mixing=False)


def ge_scale_data(particle):
    mcproduction = "single %s" % particle
    return (
        (
            ep_data("data"),
            ep_data("pythia8", "ep_ratio_1"),
        ),
        (
            (
                DataVault().input("data", histname="MassPtSM0"),
                data_feeddown(particle == "#eta"),
            ),
            (
                DataVault().input(mcproduction, "low", "PhysEff"),
                DataVault().input(mcproduction, "high", "PhysEff"),
            )
        ),
    )


@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    # "#eta",
])
def test_interface_composite(particle):
    estimator = GScale(GScaleOptions(particle=particle), plot=False)
    uncertanity = estimator.transform(
        ge_scale_data(particle),
        loggs=AnalysisOutput("test composite corr. yield interface")
    )
    Comparator().compare(uncertanity)
