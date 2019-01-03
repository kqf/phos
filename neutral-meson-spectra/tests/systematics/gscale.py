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


GE_SCALE_DATA = Proxy(
    lambda:
    (
        (
            ep_data("data"),
            ep_data("pythia8", "ep_ratio_1"),
        ),
        (
            (
                DataVault().input("data", histname="MassPtSM0"),
                data_feeddown(),
            ),
            (
                DataVault().input("single #pi^{0}", "low", "PhysEff"),
                DataVault().input("single #pi^{0}", "high", "PhysEff"),
            )
        ),
    )
)


@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.interactive
def test_interface_composite():
    estimator = GScale(GScaleOptions(particle="#pi^{0}"), plot=False)
    uncertanity = estimator.transform(
        GE_SCALE_DATA,
        loggs=AnalysisOutput("test composite corr. yield interface")
    )
    Comparator().compare(uncertanity)
