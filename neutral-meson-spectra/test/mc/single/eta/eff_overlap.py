import unittest

from spectrum.options import Options
from spectrum.efficiency import Efficiency
from spectrum.comparator import Comparator
from spectrum.broot import BROOT as br
from test.mc.single.eff_overlap import TestOverlapRegion

# TODO: Change pt region for eta mesons
class TestOverlapRegionEta(TestOverlapRegion):


    def setUp(self):
        self.eff_title = '#varepsilon = #Delta #phi #Delta y/ 2 #pi '\
                         '#frac{Number of reconstructed #eta}{Number of generated primary #eta}'


    def test_eff_overlap(self):
        files = {
            DataVault().file("single #eta", "low"): (0, 5),
            DataVault().file("single #eta", "high"): (9, 20)
        }
        
        self.efficiency_overlap(files, 'weight1', 'eta')

