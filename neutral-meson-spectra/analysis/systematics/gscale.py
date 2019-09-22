import pytest

from spectrum.output import open_loggs
from spectrum.comparator import Comparator

from spectrum.uncertainties.gscale import GScale
from spectrum.uncertainties.gscale import GScaleOptions
from spectrum.uncertainties.gscale import ge_scale_data


# Benchmark:
# In the 5 TeV analysis U_ge ~ 0.01 - 0.03

@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta",
])
def test_interface_composite(particle):
    estimator = GScale(GScaleOptions(particle=particle), plot=False)
    with open_loggs() as loggs:
        uncertanity = estimator.transform(ge_scale_data(particle), loggs)
    Comparator().compare(uncertanity)
