import pytest

from spectrum.output import open_loggs
from spectrum.comparator import Comparator

from spectrum.uncertainties.yields import YieldExtractioin
from spectrum.uncertainties.yields import YieldExtractioinUncertanityOptions
from spectrum.uncertainties.yields import yield_extraction_data


# Benchmark:
# In the 5 TeV analysis U_extraction ~ 0.08 - 0.05
# For eta meson @ 7 TeV it's ~ 0.25
# For eta meson @ 5 TeV it's ~ 0.10

@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle", [
    # "#pi^{0}",
    "#eta",
])
def test_yield_extraction_uncertanity_pion(particle):
    estimator = YieldExtractioin(
        YieldExtractioinUncertanityOptions(particle=particle)
    )
    with open_loggs("cyield uncertainty", shallow=True) as loggs:
        output = estimator.transform(
            yield_extraction_data(particle=particle),
            loggs
        )
    Comparator().compare(output)
