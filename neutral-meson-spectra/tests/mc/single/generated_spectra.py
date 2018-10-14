import unittest
from spectrum.input import read_histogram
from spectrum.comparator import Comparator
from spectrum.broot import BROOT as br


class TestGeneratedSpectra(unittest.TestCase):

    def test_spectra(self):
        datapath = 'single/nonlin0/'

        pi0 = read_histogram(datapath + 'LHC17j3b1.root',
                             'PhysEffTender', 'hPtLong_#pi^{0}', '#pi^{0}')
        eta = read_histogram(datapath + 'LHC17j3c1.root',
                             'PhysEffTender', 'hPtLong_#eta', '#eta')

        for e in (eta, pi0):
            br.scalew(e, 1. / e.Integral())
            e.logx = True
            e.logy = True
            e.SetAxisRange(0, 10, "X")

        diff = Comparator(
            rrange=(0.8, 1.2)
        )
        diff.compare(eta, pi0)
