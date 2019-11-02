import pytest

from spectrum.spectra import spectrum
from spectrum.output import open_loggs
from spectrum.input import SingleHistInput
from spectrum.plotter import plot
from spectrum.constants import invariant_cross_section_code
import spectrum.broot as br
from vault.datavault import DataVault

HISTNAMES = {
    "#pi^{0}": "hxsPi0PtInv",
    "#eta": "hxsEtaPtInv"
}


@pytest.fixture
def pythia6(particle):
    data = DataVault().input("theory", "pythia6")
    with open_loggs() as loggs:
        mc = SingleHistInput(HISTNAMES[particle]).transform(data, loggs)
        mc.Scale(1e-6)
        mc.SetTitle("PYTHIA 6")
    return mc


def ratio(hist, func):
    param = br.function2histogram(func, hist)
    return br.ratio(hist, param)


@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta"
])
def test_compare_with_pythia(pythia6, particle, tcm, oname):
    cs = spectrum(particle)
    cs.SetTitle("Data")
    cs.Fit(tcm, "RQ")
    plot(
        [cs, pythia6, tcm],
        ytitle=invariant_cross_section_code(),
        xtitle="p_{T} (GeV/#it{c})",
        xlimits=(2, 22),
        ylimits=(0.0002, 400),
        csize=(96, 128),
        ltitle="{} #rightarrow #gamma#gamma".format(particle),
        legend_pos=(0.65, 0.7, 0.8, 0.88),
        yoffset=1.4,
        more_logs=False,
        oname=oname.format("pythia/"),
    )
