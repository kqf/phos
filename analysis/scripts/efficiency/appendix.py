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
    low = loggs['steps']['analysis-0']["invmasses"]["output"].masses
    high = loggs['steps']['analysis-1']["invmasses"]["output"].masses
    low = [l for l in low if l["pt_range"][-1] < 7]
    high = [h for h in high if h["pt_range"][0] > 7]
    MultiplePlotter(oname, no_stats=True).transform(low + high, stop=stop)
