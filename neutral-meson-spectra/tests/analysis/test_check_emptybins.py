import pytest

from spectrum.vault import DataVault
from spectrum.pipeline import ComparePipeline
from spectrum.analysis import Analysis
from spectrum.options import Options
from spectrum.output import open_loggs


# Problem: There are some bins in invariant mass histogram
#          that have no entries for same event data and
#          nonzero content for mixed event. ROOT fails to calculate
#          the error in that bin for real/mixed ratio!
#
#          This test compares different solutions
#

@pytest.fixture
def data():
    return (DataVault().input("data", histname="MassPtSM0"), ) * 2


@pytest.mark.onlylocal
@pytest.mark.skip("This analysis is outdated always use standard method")
def test_check_empty_bins(data):
    options = []
    for average in ["standard", "with empty"]:
        option = Options()
        option.invmass.average = average
        options.append(option)

    estimator = ComparePipeline([
        (o.invmass.average, Analysis(o)) for o in options
    ], plot=True)

    with open_loggs("check empty bins") as loggs:
        estimator.transform(data, loggs)
