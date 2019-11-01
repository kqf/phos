import pytest

from spectrum.spectra import ratio as sratio
from spectrum.output import open_loggs
from spectrum.input import SingleHistInput
from spectrum.comparator import Comparator
import spectrum.broot as br
from vault.datavault import DataVault
from vault.formulas import FVault

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


@pytest.mark.skip("")
@pytest.mark.onlylocal
@pytest.mark.interactive
def test_ratio(data):
    rdata = sratio()
    rdata.logy = True
    rdata.logx = True
    rdata.label = "data, pp #sqrt{s} = 13 TeV"
    rdata.SetTitle("")

    with open_loggs() as loggs:
        mc = br.ratio(
            SingleHistInput(HISTNAMES["#eta"]).transform(data, loggs),
            SingleHistInput(HISTNAMES["#pi^{0}"]).transform(data, loggs)
        )
        mc.label = "pythia6"
        mc.SetTitle("")

    histograms = [rdata] + [mc]
    for rr in histograms:
        rr.GetYaxis().SetTitle("#eta / #pi^{0}")
        rr.GetXaxis().SetTitle("p_{T}")
        # rr.GetYaxis().SetRangeUser(0, 10)
    Comparator().compare(histograms)
