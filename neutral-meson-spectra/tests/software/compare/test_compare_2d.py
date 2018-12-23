import ROOT
from spectrum.comparator import Comparator


def test_draws_2d_hist(data, stop):
    hist = ROOT.TH2F("h2d", "Testing 2D comparison", 20, 0, 5, 20, 0, 5)
    for i in range(1, 5):
        for j in range(1, 5):
            hist.Fill(i, j, i)
    Comparator(stop=stop).compare(hist)
