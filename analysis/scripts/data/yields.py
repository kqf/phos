import pytest

import spectrum.broot as br
from spectrum.output import open_loggs
from spectrum.options import Options
from spectrum.analysis import Analysis
from spectrum.plotter import plot


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
def test_spectrum(particle, data, oname, ltitle, stop):
    options = Options(particle=particle)
    with open_loggs() as loggs:
        spectrum = Analysis(options).transform(data, loggs).spectrum

    spectrum.SetTitle("Data")
    plot(
        [spectrum],
        stop=stop,
        ltitle=ltitle,
        oname=oname,
        more_logs=False,
    )
