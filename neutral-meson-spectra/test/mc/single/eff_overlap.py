import unittest

from spectrum.options import Options
from spectrum.efficiency import Efficiency
from spectrum.comparator import Comparator
from spectrum.broot import BROOT as br


class TestOverlapRegion(unittest.TestCase):


    def setUp(self):
        self.eff_title = ""

        
    def efficiency_overlap(self, files, pref, particle):
        plabel = "#pi^{0}" if particle == 'pi0' else '#eta'
        labels = {'1': 'low p_{T}', '2': 'high p_{T}'}
        estimators = [Efficiency('hPt_%s_primary_' % plabel, labels[f[-1]], f) for f in files]

        # Set Custom Fit Range
        for est, rr in zip(estimators, files.values()):
            est.selection = 'PhysEffPlainOnlyTender'
            est.opt = Options.spmc(rr, particle = particle)

        self.check_range(estimators, pref)


    def check_range(self, estimators, pref):
        # Define compare options
        diff = Comparator(rrange = (-1, -1), crange = (0, 0.016),
            oname = 'compared-efficiency-{0}'.format(pref))
        effs = [e.eff() for e in estimators]

        # Avoid problem with negative values
        for e in effs: 
            e.Scale(1./ 4. * 0.3)
            e.SetTitle(self.eff_title)
            e.GetYaxis().SetTitle('efficiency #times acceptance')
            e.logy = 0

        diff.compare(effs)
