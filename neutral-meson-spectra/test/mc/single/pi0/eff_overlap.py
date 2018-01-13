import unittest

from spectrum.efficiency import Efficiency
from spectrum.comparator import Comparator
from spectrum.broot import BROOT as br
from test.mc.single.eff_overlap import TestOverlapRegion


class TestOverlapRegionPi0(TestOverlapRegion):


    def setUp(self):
        self.eff_title = '#varepsilon = #Delta #phi #Delta y/ 2 #pi ' \
                         '#frac{Number of reconstructed #pi^{0}}{Number of generated primary #pi^{0}}'


    def test_eff_overlap(self):
        ddir = 'single/nonlin0/'
        files = {
                    ddir + 'LHC17j3b1': (0, 5),
                    ddir + 'LHC17j3b2': (9, 20)
                }

        self.efficiency_overlap(files, 'weight1', 'pi0')