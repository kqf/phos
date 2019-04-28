import pytest

from spectrum.output import AnalysisOutput
from uncertainties.tof import TofUncertainty, TofUncertaintyOptions
from uncertainties.tof import tof_data

# from spectrum.comparator import Comparator


@pytest.mark.thesis
@pytest.mark.interactive
@pytest.mark.onlylocal
def test_tof():
    tof = TofUncertainty(TofUncertaintyOptions())
    loggs = AnalysisOutput("tof uncertainty")
    output = tof.transform(tof_data(), loggs=loggs)
    loggs.plot()
    assert len(output) > 0
