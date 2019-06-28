import pytest

from spectrum.options import CompositeCorrectedYieldOptions
from spectrum.output import open_loggs
from uncertainties.yields import YieldExtractioin, yield_extraction_data
from uncertainties.yields import YieldExtractioinUncertanityOptions
from spectrum.comparator import Comparator


@pytest.mark.thesis
@pytest.mark.interactive
@pytest.mark.onlylocal
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta",
])
def test_yield_extraction_uncertanity_pion(particle):
    options = YieldExtractioinUncertanityOptions(
        CompositeCorrectedYieldOptions(particle=particle)
    )
    estimator = YieldExtractioin(options)
    with open_loggs() as loggs:
        output = estimator.transform(
            yield_extraction_data(particle=particle),
            loggs
        )
    Comparator().compare(output)
