import pytest

from spectrum.output import open_loggs
from uncertainties.tof import TofUncertainty, TofUncertaintyOptions
from uncertainties.tof import tof_data

# from spectrum.comparator import Comparator


@pytest.fixture
def data():
    return tof_data()


@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.interactive
def test_tof(data):
    tof = TofUncertainty(TofUncertaintyOptions())
    with open_loggs("tof uncertainty") as loggs:
        output = tof.transform(data, loggs)
    assert len(output) > 0
