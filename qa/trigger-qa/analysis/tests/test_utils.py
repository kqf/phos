import pytest
import ROOT
from trigger.utils import trendhist
from trigger.utils import sumhists
from random import shuffle


def test_trend_hist(nbins=100):
    bins = range(2000, 2201)
    shuffle(bins)
    print bins
    contents = [b + 1 for b in bins]
    trendhist(bins, contents)


@pytest.mark.parametrize("size", [2, 3, 5, 10])
def test_sums_hists(size):
    hists = [ROOT.TH1F("t{}".format(s), "", 100, 0, 100) for s in range(size)]
    for h in hists:
        h.FillRandom("gaus")

    total = sumhists(hists)
    assert total.GetEntries() == sum(map(lambda x: x.GetEntries(), hists))
