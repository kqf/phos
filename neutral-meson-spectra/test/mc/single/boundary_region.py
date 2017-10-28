import unittest

from spectrum.efficiency import Efficiency, EfficiencyMultirange
from spectrum.comparator import Comparator
from spectrum.broot import BROOT as br


class TestOverlapRegion(unittest.TestCase):


    def test_calculate_check_overlap(self):
        files = ['LHC17j3b1', 'LHC17j3b2']

        ranges = [(0, 6), (8, 20)],
        estimators = [Efficiency('hPt_#pi^{0}_primary_', f, f) for f in files]

        for pt_range in ranges:
            self.check_range(estimators, pt_range)


    def check_range(self, estimators, ranges):
        # Set Custom Fit Range
        for est, rr in zip(estimators, ranges):
            est.opt.spectrum.fit_range = rr

        # Define compare options
        diff = Comparator(rrange = (-1, -1), crange = (0, 0.2))
        effs = [e.eff() for e in estimators]

        # Avoid problem with negative values
        for e in effs: 
            e.logy = 0

        diff.compare(effs)

