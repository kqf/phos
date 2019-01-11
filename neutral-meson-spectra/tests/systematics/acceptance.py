import pytest
from vault.datavault import DataVault
from spectrum.output import AnalysisOutput
from uncertainties.acceptance import Acceptance, AcceptanceOptions
from spectrum.comparator import Comparator
from tools.feeddown import data_feeddown


def cyield_data(particle):
    mc_production = "single %s" % particle
    data_input = (
        DataVault().input("data", histname="MassPtSM0"),
        data_feeddown(),
    )
    mc_inputs = (
        DataVault().input(mc_production, "low", listname="PhysEff"),
        DataVault().input(mc_production, "high", listname="PhysEff"),
    )
    return data_input, mc_inputs


def acceptance_data(particle):
    return (
        cyield_data(particle),
        (
            cyield_data(particle),
            cyield_data(particle),
        ),
    )


@pytest.mark.thesis
@pytest.mark.interactive
@pytest.mark.onlylocal
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    # "#eta"
])
def test_acceptance(particle):
    estimator = Acceptance(
        AcceptanceOptions(particle=particle), plot=False)
    uncertanity = estimator.transform(
        acceptance_data(particle),
        loggs=AnalysisOutput("uncertainty acceptance")
    )
    Comparator().compare(uncertanity)
