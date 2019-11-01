import pytest

from spectrum.spectra import spectrum
from spectrum.output import open_loggs
from spectrum.input import SingleHistInput
from spectrum.comparator import Comparator
import spectrum.broot as br
from vault.datavault import DataVault
from vault.formulas import FVault
import spectrum.sutils as su

HISTNAMES = {
    "#pi^{0}": "hxsPi0PtInv",
    "#eta": "hxsEtaPtInv"
}


@pytest.fixture
def data():
    return DataVault().input("theory", "pythia6")


def ratio(hist, particle):
    param = br.function2histogram(
        FVault().tf1("tcm", "{} 13 TeV".format(particle)),
        hist)
    return br.ratio(hist, param)


@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta"
])
def test_compare_with_pythia(data, particle):
    cyield = spectrum(particle)
    cyield.logy = True
    cyield.logx = True
    cyield.label = "data, pp #sqrt{s} = 13 TeV"
    cyield.SetTitle("")

    with open_loggs() as loggs:
        mc = SingleHistInput(HISTNAMES[particle]).transform(data, loggs)
        mc.Scale(1e-6)
        mc.label = "pythia6"
        mc.SetTitle("")

    with su.canvas():
        cyield.Draw()
        func = FVault().tf1("tcm", "{} 13 TeV".format(particle))
        func.Draw("same")

    histograms = [cyield] + [mc]
    Comparator().compare(histograms)
    ratios = [ratio(h, particle) for h in histograms]
    for rr in ratios:
        rr.GetYaxis().SetTitle("#frac{Data, pythia}{TCM fit}")
        rr.GetYaxis().SetRangeUser(0, 10)
        rr.logx = False
        rr.logy = False
    Comparator().compare(ratios)
