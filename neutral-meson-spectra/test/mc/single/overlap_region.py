import unittest

from spectrum.efficiency import Efficiency, EfficiencyMultirange
from spectrum.comparator import Comparator
from spectrum.broot import BROOT as br


class TestOverlapRegion(unittest.TestCase):


    def test_eff_overlap(self):
        ddir = 'single/plain/'
        files = {
                    ddir + 'LHC17j3b1': (0, 6),
                    ddir + 'LHC17j3b2': (8, 20)
                }

        self.efficiency_overlap(files)

        ddir = 'single/nonlin/'
        files = {
                    ddir + 'LHC17j3b1': (0, 6),
                    ddir + 'LHC17j3b2': (8, 20)
                }
        self.efficiency_overlap(files)


    def efficiency_overlap(self, files):
        estimators = [Efficiency('hPt_#pi^{0}_primary_', f, f) for f in files]

        # Set Custom Fit Range
        for est, rr in zip(estimators, files.values()):
            est.opt.spectrum.fit_range = rr

        self.check_range(estimators)

    def check_range(self, estimators):
        # Define compare options
        diff = Comparator(rrange = (-1, -1), crange = (0, 0.2))
        effs = [e.eff() for e in estimators]

        # Avoid problem with negative values
        for e in effs: 
            e.logy = 0

        diff.compare(effs)

