import pytest

from spectrum.output import AnalysisOutput
from uncertainties.tof import TofUncertainty, TofUncertaintyOptions
from vault.datavault import DataVault

# from spectrum.comparator import Comparator

TOF_DATASET = (
    DataVault().input("data", histname="MassPtSM0"),
    DataVault().input("data", "isolated", histname="MassPtSM0"),
)

STABLE_TOF_DATASET = (
    DataVault().input("data", "stable"),
    DataVault().input("data", "isolated", histname="MassPtSM0"),
)


@pytest.mark.interactive
@pytest.mark.onlylocal
def test_tof():
    tof = TofUncertainty(TofUncertaintyOptions())
    loggs = AnalysisOutput("tof uncertainty")
    output = tof.transform(STABLE_TOF_DATASET, loggs=loggs)
    loggs.plot()
    assert len(output) > 0
