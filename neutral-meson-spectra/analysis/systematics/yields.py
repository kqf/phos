import pytest

from spectrum.output import open_loggs
from spectrum.comparator import Comparator

from spectrum.uncertainties.yields import YieldExtractioin
from spectrum.uncertainties.yields import YieldExtractioinUncertanityOptions
from spectrum.uncertainties.yields import yield_extraction_data


# Benchmark:
# In the 5 TeV analysis U_extraction ~ 0.08 - 0.05

@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    # "#eta",
])
def test_yield_extraction_uncertanity_pion(particle):
    estimator = YieldExtractioin(
        YieldExtractioinUncertanityOptions(particle=particle)
    )
    # nsigma = 3, cball, mid, pol1
    # nsigma = 3, gaus, mid, pol1
    # nsigma = 2, gaus, wide, pol1
    # nsigma = 2, cball, mid, pol1
    # nsigma = 2, gaus, mid, pol1
    with open_loggs("cyield uncertainty", shallow=True) as loggs:
        output = estimator.transform(
            yield_extraction_data(particle=particle),
            loggs
        )
    Comparator().compare(output)
