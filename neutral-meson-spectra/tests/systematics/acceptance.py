import pytest
from vault.datavault import DataVault
from spectrum.output import AnalysisOutput
from uncertainties.acceptance import Acceptance, AcceptanceOptions
from spectrum.comparator import Comparator
from tools.feeddown import data_feeddown


def cyield_data(particle, cut):
    mc_production = "single %s acceptance" % particle
    data_input = (
        DataVault().input(
            "data", "acceptance",
            listname="Phys{}".format(cut),
            histname="MassPtSM0"),
        data_feeddown(),
    )
    mc_inputs = (
        DataVault().input(
            mc_production, "low",
            listname="PhysEff{}".format(cut),
            # histname="MassPtSM0"
        ),
        DataVault().input(
            mc_production, "high",
            listname="PhysEff{}".format(cut),
            # histname="MassPtSM0"
        ),
    )
    return data_input, mc_inputs


def acceptance_data(particle):
    return (
        cyield_data(particle, cut=0),
        (
            cyield_data(particle, cut=1),
            cyield_data(particle, cut=2),
            cyield_data(particle, cut=3),
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
    loggs = AnalysisOutput("uncertainty acceptance")
    uncertanity = estimator.transform(
        acceptance_data(particle),
        loggs=loggs
    )
    Comparator().compare(uncertanity)
    loggs.plot()
