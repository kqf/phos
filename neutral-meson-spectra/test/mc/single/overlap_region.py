import unittest

from spectrum.options import Options
from spectrum.efficiency import Efficiency
from spectrum.comparator import Comparator
from spectrum.broot import BROOT as br


# TODO: Change pt region for eta mesons
class TestOverlapRegion(unittest.TestCase):


    def setUp(self):
        self.eff_title = '#varepsilon = #Delta #phi #Delta y/ 2 #pi #frac{Number of reconstructed #pi^{0}}{Number of generated primary #pi^{0}}'


    def test_eff_overlap(self):
        ddir = 'single/nonlin0/'
        files = {
                    ddir + 'LHC17j3b1': (0, 5),
                    ddir + 'LHC17j3b2': (9, 20)
                }

        # self.efficiency_overlap(files, 'weight1', 'pi0')

        ddir = 'single/nonlin0/'
        files = {
                    ddir + 'LHC17j3c1': (0, 7),
                    ddir + 'LHC17j3c2': (6, 20)
                }

        self.efficiency_overlap(files, 'weight1', 'eta')



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

