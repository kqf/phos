import pytest

import spectrum.broot as br
from spectrum.output import open_loggs
from spectrum.comparator import Comparator

from spectrum.uncertainties.acceptance import Acceptance
from spectrum.uncertainties.acceptance import AcceptanceOptions
from spectrum.uncertainties.acceptance import acceptance_data

# Benchmark:
# In the 5 TeV analysis U_accept ~ 0.018


@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    # "#eta"
])
def test_acceptance(particle, stop):
    estimator = Acceptance(
        AcceptanceOptions(particle=particle),
        plot=stop)

    with open_loggs() as loggs:
        uncertanity = estimator.transform(acceptance_data(particle), loggs)

        print(
            "\def \{}AcceptanceUncertainty {{{:.2f}}}".format(
                br.spell(particle),
                br.bins(uncertanity).contents.mean() * 100
            )
        )
        Comparator(stop=stop).compare(uncertanity)
