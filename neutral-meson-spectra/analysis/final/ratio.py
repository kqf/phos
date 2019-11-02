import pytest

from spectrum.spectra import ratio as sratio
from spectrum.comparator import Comparator


@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.interactive
def test_ratio(pythia6_eta_pion_ratio):
    rdata = sratio()
    rdata.logy = False
    rdata.logx = False
    rdata.label = "data, pp #sqrt{s} = 13 TeV"
    rdata.SetTitle("")
    histograms = [rdata] + [pythia6_eta_pion_ratio]
    for rr in histograms:
        rr.GetYaxis().SetTitle("#eta / #pi^{0}")
        rr.GetXaxis().SetTitle("p_{T}")
    Comparator().compare(histograms)
