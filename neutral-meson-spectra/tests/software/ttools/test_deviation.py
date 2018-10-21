import ROOT
import unittest

from tools.deviation import MaxDeviation
from spectrum.broot import BROOT as br


class TestDeviation(unittest.TestCase):

    def test_interface(self):
        ratio = ROOT.TH1F("test", "test", 30, 0, 20)

        for i in br.range(ratio):
            ratio.SetBinContent(i, 1)
        ratio.SetBinContent(30, 1)

        ratio.SetBinContent(15, 1.5)
        ratio.SetBinContent(14, -1.3)

        output = MaxDeviation().transform(ratio, "test")
        self.assertEqual(output.GetParameter(0), 1.5 - 1.)
