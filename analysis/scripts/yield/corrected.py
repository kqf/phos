import pytest  # noqa

import spectrum.broot as br
from spectrum.options import CompositeCorrectedYieldOptions
from spectrum.cyield import CorrectedYield
from spectrum.output import open_loggs
from spectrum.plotter import plot


@pytest.fixture
def oname(particle):
    return "images/analysis/corrected_{}.pdf".format(br.spell(particle))


@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta",
])
def test_fit_the_corrected_yield(particle, cyield_data, oname):
    with open_loggs() as loggs:
        estimator = CorrectedYield(
            CompositeCorrectedYieldOptions(
                particle=particle
            )
        )
        cyield = estimator.transform(cyield_data, loggs)

    plot(
        [cyield],
        oname=oname,
        legend_pos=None,
        yoffset=1.65,
    )
