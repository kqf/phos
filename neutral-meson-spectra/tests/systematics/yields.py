import pytest

from spectrum.options import CompositeCorrectedYieldOptions
from spectrum.output import AnalysisOutput
from vault.datavault import DataVault
from uncertainties.yields import YieldExtractioin
from uncertainties.yields import YieldExtractioinUncertanityOptions
from spectrum.comparator import Comparator
from tools.feeddown import data_feeddown


def cyield_data(particle="#pi^{0}"):
    data_input = (
        DataVault().input("data", histname="MassPtSM0"),
        data_feeddown(dummy=particle == "#eta"),
    )
    production = "single %s" % particle
    mc_inputs = (
        DataVault().input(production, "low", listname="PhysEff"),
        DataVault().input(production, "high", listname="PhysEff"),
    )
    return data_input, mc_inputs


@pytest.mark.thesis
@pytest.mark.interactive
@pytest.mark.onlylocal
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta",
])
def test_yield_extraction_uncertanity_pion(particle):
    options = YieldExtractioinUncertanityOptions(
        CompositeCorrectedYieldOptions(particle=particle)
    )
    estimator = YieldExtractioin(options)
    output = estimator.transform(
        cyield_data(particle),
        loggs=AnalysisOutput("corrected yield %s" % particle)
    )
    Comparator().compare(output)
