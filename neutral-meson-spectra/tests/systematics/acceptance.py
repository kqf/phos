import pytest
from vault.datavault import DataVault
from spectrum.output import AnalysisOutput
from uncertainties.acceptance import Acceptance, AcceptanceOptions
from spectrum.comparator import Comparator
from tools.feeddown import data_feeddown


def cyield_data(data_production="data", mc_production="single #pi^{0}"):
    data_input = (
        DataVault().input(data_production, histname="MassPtSM0"),
        data_feeddown(),
    )
    mc_inputs = (
        DataVault().input(mc_production, "low", listname="PhysEff"),
        DataVault().input(mc_production, "high", listname="PhysEff"),
    )
    return data_input, mc_inputs


ACCEPTANCE_DATA = (
    cyield_data(),
    (
        cyield_data(),
        cyield_data(),
    ),
)


@pytest.mark.thesis
@pytest.mark.interactive
@pytest.mark.onlylocal
def test_acceptance():
    estimator = Acceptance(
        AcceptanceOptions(particle="#pi^{0}"), plot=False)
    uncertanity = estimator.transform(
        ACCEPTANCE_DATA,
        loggs=AnalysisOutput("test composite corr. yield interface")
    )
    Comparator().compare(uncertanity)
