import ROOT
import unittest
from math import sqrt
from uncertainties.rms import RmsToMean
from spectrum.broot import BROOT as br
from spectrum.comparator import Comparator


class TestRmsToMean(unittest.TestCase):

    def test_rms(self):
        original = ROOT.TH1F("test", "test", 30, 0, 20)
        for i in br.range(original):
            original.SetBinContent(i, 81)
        original.Sumw2()

        histograms = [original.Clone(str(i)) for i in range(9)]
        output = RmsToMean(None, False).transform(histograms, "test")
        self.assertAlmostEqual(
            output.GetBinContent(i),
            sqrt((9. / 81) ** 2 + (sqrt(9.) / 81) ** 2) / sqrt(9.)
        )
