import pytest
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


GE_SCALE_DATA = (
    (
        ep_data("data"),
        ep_data("pythia8", "ep_ratio_1"),
    ),
    (
        (
            DataVault().input("data"),
            data_feeddown(),
        ),
        (
            DataVault().input("single #pi^{0}", "low"),
            DataVault().input("single #pi^{0}", "high"),
        )
    ),
)


@pytest.mark.onlylocal
@pytest.mark.interactive
def test_interface_composite(self):
    estimator = GScale(GScaleOptions(particle="#pi^{0}"), plot=False)
    uncertanity = estimator.transform(
        GE_SCALE_DATA,
        loggs=AnalysisOutput("test composite corr. yield interface")
    )
    Comparator().compare(uncertanity)
