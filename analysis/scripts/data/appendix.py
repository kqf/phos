import pytest

import spectrum.broot as br
from spectrum.output import open_loggs
from spectrum.options import Options
from spectrum.analysis import Analysis
from spectrum.ptplotter import MultiplePlotter


@pytest.fixture
def oname(particle):
    pattern = "images/appendix_c/{}-masses"
    return pattern.format(br.spell(particle))


def change_binning(masses, particle):
    # Fix binning for the last eta bin to improve the plots
    if particle != "#eta":
        return
    data = masses[-1]
    for key in ["measured", "signal", "background"]:
        data[key].Rebin(2)
        for i in br.hrange(data[key]):
            data[key].SetBinContent(i, abs(data[key].GetBinContent(i)))


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

    change_binning(masses, particle)
    MultiplePlotter(oname, no_stats=True).transform(masses, stop=stop)
