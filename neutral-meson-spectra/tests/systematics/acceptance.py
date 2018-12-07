import pytest
from vault.datavault import DataVault
from spectrum.output import AnalysisOutput
from uncertainties.acceptance import Acceptance, AcceptanceOptions
from spectrum.comparator import Comparator


def cyield_data(data_production="data", mc_production="single #pi^{0}"):
    data_input = DataVault().input(data_production)
    mc_inputs = (
        DataVault().input(mc_production, "low"),
        DataVault().input(mc_production, "high"),
    )
    return data_input, mc_inputs


ACCEPTANCE_DATA = (
    cyield_data(),
    (
        cyield_data(),
        cyield_data(),
    ),
)


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
