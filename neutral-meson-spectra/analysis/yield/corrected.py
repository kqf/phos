import pytest  # noqa

import spectrum.broot as br
from spectrum.options import CompositeCorrectedYieldOptions
from spectrum.corrected_yield import CorrectedYield
from spectrum.output import open_loggs
from spectrum.plotter import plot


@pytest.fixture
def oname(particle):
    return "results/analysis/corrected_{}.pdf".format(br.spell(particle))


@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta",
])
def test_fit_the_corrected_yield(particle, data_cyield, oname):
    with open_loggs() as loggs:
        estimator = CorrectedYield(
            CompositeCorrectedYieldOptions(
                particle=particle
            )
        )
        cyield = estimator.transform(data_cyield, loggs)

    plot(
        [cyield],
        oname=oname,
        legend_pos=None,
        yoffset=1.65,
    )
