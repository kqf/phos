import unittest
from vault.datavault import DataVault

from spectrum.input import read_histogram
from spectrum.comparator import Comparator
from spectrum.broot import BROOT as br
from spectrum.options import Options

class TestRebin(unittest.TestCase):

    def test(self):
        infile = DataVault().file("single #pi^{0} validate", "high")

        hist = lambda x, y: read_histogram(infile, "PhysEff", x, label=y)

        binned = hist("hPt_#pi^{0}_primary_", "binned")
        standard = hist("hPt_#pi^{0}_primary_standard", "standard")

        print Options().pt.ptedges

        # return
        diff = Comparator()
        binned, standard = br.rebin_as(binned, standard)
        br.scalew(binned)
        br.scalew(standard)
        diff.compare(binned, standard)
