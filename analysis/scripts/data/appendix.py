import pytest

import spectrum.broot as br
from spectrum.output import open_loggs
from spectrum.options import Options
from spectrum.analysis import Analysis
from spectrum.ptplotter import MultiplePlotter


@pytest.fixture
def oname(particle):
    pattern = "images/analysis/data/{}.pdf"
    return pattern.format(br.spell(particle))


@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta"
])
def test_invmasses(particle, data, oname, ltitle, stop):
    options = Options(particle=particle)
    with open_loggs() as loggs:
        Analysis(options).transform(data, loggs)
    masses = loggs["invmasses"]["output"].masses
    print(len(masses))
    MultiplePlotter(no_stats=True).transform(masses, stop=stop)
