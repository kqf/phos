import pytest

from spectrum.options import CompositeCorrectedYieldOptions
from spectrum.output import AnalysisOutput
from vault.datavault import DataVault
from uncertainties.yields import YieldExtractioin
from uncertainties.yields import YieldExtractioinUncertanityOptions
from spectrum.comparator import Comparator

EFFICIENCY_DATA = (
    DataVault().input("single #pi^{0}", "low"),
    DataVault().input("single #pi^{0}", "high"),
)

CYIELD_DATA = (
    DataVault().input("data"),
    EFFICIENCY_DATA
)


@pytest.mark.interactive
@pytest.mark.onlylocal
def test_yield_extraction_uncertanity_pion():

    options = YieldExtractioinUncertanityOptions(
        CompositeCorrectedYieldOptions(particle="#pi^{0}")
    )
    estimator = YieldExtractioin(options)
    output = estimator.transform(
        CYIELD_DATA,
        loggs=AnalysisOutput("corrected yield #pi^{0}")
    )
    Comparator().compare(output)
