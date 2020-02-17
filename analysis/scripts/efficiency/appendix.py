import pytest

import spectrum.broot as br
from spectrum.output import open_loggs
from spectrum.options import CompositeOptions
from spectrum.analysis import Analysis
from spectrum.ptplotter import MultiplePlotter


@pytest.fixture
def oname(particle):
    pattern = "images/appendix_c/{}-masses"
    return pattern.format(br.spell(particle))


@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta"
])
def test_invmasses(particle, spmc, oname, ltitle, stop):
    options = CompositeOptions(particle=particle)
    with open_loggs() as loggs:
        Analysis(options).transform(spmc, loggs)
    masses = loggs['steps']['analysis-0']["invmasses"]["output"].masses
    MultiplePlotter(oname, no_stats=True).transform(masses, stop=stop)
