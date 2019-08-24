import pytest

from spectrum.output import open_loggs
from spectrum.comparator import Comparator  # noqa

from spectrum.uncertainties.tof import TofUncertainty
from spectrum.uncertainties.tof import TofUncertaintyOptions
from spectrum.uncertainties.tof import tof_data


@pytest.fixture
def data():
    return tof_data()


# Benchmark:
# In the 5 TeV analysis U_tof ~ 0.02

@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.interactive
def test_tof(data):
    tof = TofUncertainty(TofUncertaintyOptions())
    with open_loggs("tof") as loggs:
        output = tof.transform(data, loggs)
    assert len(output) > 0
