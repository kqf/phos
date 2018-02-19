import unittest

# from spectrum.spectrum import Spectrum 
from spectrum.input import Input 
from spectrum.options import Options 
from spectrum.efficiency import Efficiency
from spectrum.corrected_yield import CorrectedYield
from spectrum.efficiency import EfficiencyMultirange

from spectrum.comparator import Comparator
from spectrum.broot import BROOT as br
from vault.datavault import DataVault



class YieldEvaluator(object):


    def __init__(self, particle):
        super(YieldEvaluator, self).__init__()
        self.particle= particle


    def efficiency(self, fileranges):
        efficiency_estimator = EfficiencyMultirange(
            'hPt_{0}_primary_'.format(self.particle),
            'efficiency',
            fileranges,
            particle=self.particle
        )

        efficiency = efficiency_estimator.eff()
        efficiency.SetTitle(
            '#varepsilon = #Delta #phi #Delta y/ 2 #pi ' \
            '#frac{Number of reconstructed %s}{Number of generated primary %s}' \
            % (self.particle, self.particle) 
        )
        diff = Comparator()
        diff.compare(efficiency)
        return efficiency


    def transform(self, inp, eff_files):
        eff = self.efficiency(eff_files)
        cy_estimator = CorrectedYield(inp, Options(), eff)
        corrected_spectrum = cy_estimator.evaluate() 
        return corrected_spectrum


class TestCorrectedYield(unittest.TestCase):

    def test_interface(self):
        inp = Input(DataVault().file("data"), 'Phys', label='data')
        estimator = YieldEvaluator("#pi^{0}")

        files = {
            DataVault().file("single #pi^{0}", "low"): (0, 7),
            DataVault().file("single #pi^{0}", "high"): (7, 20)
        } 
        corrected = estimator.transform(inp, files)

        diff = Comparator()
        diff.compare(corrected)

