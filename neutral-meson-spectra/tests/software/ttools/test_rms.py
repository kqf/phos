import ROOT
import pytest
from math import sqrt
from tools.rms import RmsToMean
from spectrum.broot import BROOT as br


def test_rms():
    original = ROOT.TH1F("test", "test", 30, 0, 20)
    for i in br.range(original):
        original.SetBinContent(i, 81)
    original.Sumw2()

    histograms = [original.Clone(str(i)) for i in range(9)]
    output = RmsToMean(None, False).transform(histograms, "test")
    assert pytest.approx(output.GetBinContent(i)) == sqrt(
        (9. / 81) ** 2 + (sqrt(9.) / 81) ** 2) / sqrt(9.)
