import pytest

from spectrum.spectra import energies
from spectrum.plotter import plot
from spectrum.constants import invariant_cross_section_code
import spectrum.broot as br


@pytest.fixture
def data(particle):
    spectra = sorted(energies(particle), key=lambda x: x.energy)
    for i, cs in enumerate(spectra):
        cs.Scale(10 ** i)
        cs.SetTitle(cs.GetTitle() + " #times 10^{{{}}}".format(i))
    return spectra[::-1]


@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta",
])
def test_downloads_from_hepdata(particle, data, ltitle, oname):
    tot = br.bins(data[0].tot)
    print()
    print(
        "\def \\{}AverageTotalError{{{:.0f}}}".format(
            br.spell(particle),
            (tot.errors / tot.contents).mean() * 100)
    )
    plot(
        data,
        ytitle=invariant_cross_section_code(),
        xtitle="#it{p}_{T} (GeV/#it{c})",
        logx=False,
        ltitle=ltitle,
        legend_pos=(0.55, 0.65, 0.7, 0.85),
        oname=oname.format("/energies/")
    )
