import pytest

from spectrum.spectra import spectrum
from spectrum.output import open_loggs
from spectrum.input import SingleHistInput
from spectrum.comparator import Comparator
from spectrum.broot import BROOT as br
from vault.datavault import DataVault
from vault.formulas import FVault


@pytest.fixture
def data():
    return DataVault().input("theory", "pythia6")


@pytest.fixture
def histname(particle):
    return {
        "#pi^{0}": "hxsPi0PtInv",
        "#eta": "hxsEtaPtInv"
    }.get(particle)


def ratio(hist, particle):
    param = br.function2histogram(
        FVault().tf1("tsallis", "{} 13 TeV".format(particle)),
        hist)
    return br.ratio(hist, param)


@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta"
])
def test_simple(data, particle, histname):
    cyield = spectrum(particle)
    cyield.logy = True
    cyield.logx = True

    with open_loggs() as loggs:
        mc = SingleHistInput(histname).transform(data, loggs)
        mc.Scale(1e-6)

    histograms = [cyield] + [mc]
    Comparator().compare(histograms)

    ratios = [ratio(h, particle) for h in histograms]
    Comparator().compare(ratios)
