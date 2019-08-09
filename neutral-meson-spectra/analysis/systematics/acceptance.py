import pytest

from spectrum.output import open_loggs
from spectrum.comparator import Comparator

from spectrum.uncertainties.acceptance import Acceptance
from spectrum.uncertainties.acceptance import AcceptanceOptions
from spectrum.uncertainties.acceptance import acceptance_data


@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    # "#eta"
])
def test_acceptance(particle):
    estimator = Acceptance(
        AcceptanceOptions(particle=particle),
        plot=False)

    with open_loggs("acceptance") as loggs:
        uncertanity = estimator.transform(acceptance_data(particle), loggs)
        Comparator().compare(uncertanity)
