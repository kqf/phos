import unittest

from spectrum.efficiency import Efficiency
from spectrum.comparator import Comparator
from spectrum.broot import BROOT as br


class TestOverlapRegion(unittest.TestCase):


    def setUp(self):
        self.eff_title = '#varepsilon =  #frac{Number of reconstructed #pi^{0}}{Number of generated primary #pi^{0}}'


    def test_eff_overlap(self):
        ddir = 'single/weight0/'
        files = {
                    ddir + 'LHC17j3b1': (0, 6),
                    ddir + 'LHC17j3b2': (8, 20)
                }

        self.efficiency_overlap(files, 'weight0')


    def efficiency_overlap(self, files, pref):
        labels = {'1': 'low p_{T}', '2': 'high p_{T}'}
        estimators = [Efficiency('hPt_#pi^{0}_primary_', labels[f[-1]], f) for f in files]

        # Set Custom Fit Range
        for est, rr in zip(estimators, files.values()):
            est.selection = 'PhysEffOnlyTender'
            est.opt.spectrum.fit_range = rr
            est.opt.param.fit_range = [0.1, 0.2]

        self.check_range(estimators, pref)

    def check_range(self, estimators, pref):
        # Define compare options
        diff = Comparator(rrange = (-1, -1), crange = (0, 0.2),
            oname = 'compared-efficiency-{0}'.format(pref))
        effs = [e.eff() for e in estimators]

        # Avoid problem with negative values
        for e in effs: 
            e.SetTitle(self.eff_title)
            e.GetYaxis().SetTitle('efficiency #times acceptance')
            e.logy = 0

        diff.compare(effs)

