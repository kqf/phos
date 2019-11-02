import pytest

from spectrum.spectra import spectrum
from spectrum.output import open_loggs
from spectrum.input import SingleHistInput
from spectrum.plotter import plot
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
def test_compare_with_pythia(pythia6, particle, tcm):
    cs = spectrum(particle)
    cs.SetTitle("Data")
    cs.Fit(tcm, "RQ")
    plot([cs, pythia6, tcm])
