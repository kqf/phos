import pytest
from spectrum.output import open_loggs
from uncertainties.gscale import GScale, GScaleOptions, ge_scale_data
from spectrum.comparator import Comparator


@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    # "#eta",
])
def test_interface_composite(particle):
    estimator = GScale(GScaleOptions(particle=particle), plot=False)
    with open_loggs() as loggs:
        uncertanity = estimator.transform(ge_scale_data(particle), loggs)
    Comparator().compare(uncertanity)
