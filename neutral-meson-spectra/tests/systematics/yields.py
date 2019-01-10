import pytest

from spectrum.options import CompositeCorrectedYieldOptions
from spectrum.output import AnalysisOutput
from vault.datavault import DataVault
from uncertainties.yields import YieldExtractioin
from uncertainties.yields import YieldExtractioinUncertanityOptions
from spectrum.comparator import Comparator
from tools.feeddown import data_feeddown


def cyield_data():
    data_input = (
        DataVault().input("data", histname="MassPtSM0"),
        data_feeddown(),
    )
    mc_inputs = (
        DataVault().input("single #pi^{0}", "low", listname="PhysEff"),
        DataVault().input("single #pi^{0}", "high", listname="PhysEff"),
    )
    return data_input, mc_inputs


@pytest.mark.thesis
@pytest.mark.interactive
@pytest.mark.onlylocal
def test_yield_extraction_uncertanity_pion():
    options = YieldExtractioinUncertanityOptions(
        CompositeCorrectedYieldOptions(particle="#pi^{0}")
    )
    estimator = YieldExtractioin(options)
    output = estimator.transform(
        cyield_data(),
        loggs=AnalysisOutput("corrected yield #pi^{0}")
    )
    Comparator().compare(output)
