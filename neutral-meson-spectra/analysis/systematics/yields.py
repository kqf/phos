import pytest

from spectrum.options import CompositeCorrectedYieldOptions
from spectrum.output import open_loggs
from spectrum.comparator import Comparator

from spectrum.uncertainties.yields import YieldExtractioin,
from spectrum.uncertainties.yields import YieldExtractioinUncertanityOptions
from spectrum.uncertainties.yields import yield_extraction_data


@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    # "#eta",
])
def test_yield_extraction_uncertanity_pion(particle):
    options = YieldExtractioinUncertanityOptions(
        CompositeCorrectedYieldOptions(particle=particle)
    )
    estimator = YieldExtractioin(options)
    with open_loggs("cyield uncertainty") as loggs:
        output = estimator.transform(
            yield_extraction_data(particle=particle),
            loggs
        )
        Comparator().compare(output)
