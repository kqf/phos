import unittest

# from spectrum.spectrum import Spectrum 
from spectrum.input import Input 
from spectrum.options import Options 
from spectrum.efficiency import Efficiency
from spectrum.corrected_yield import CorrectedYield

from spectrum.comparator import Comparator


class TestCorrectedYield(unittest.TestCase):

    def test_interface(self):
       inp, opt = Input('LHC16.root', 'PhysTender'), Options('data', 'q')
       eff = Efficiency('hPt_#pi^{0}_primary_', 'eff', 'Pythia-LHC16-a5').eff()
       cy_estimator = CorrectedYield(inp, opt, eff)

       corrected_spectrum = cy_estimator.evaluate()

       diff = Comparator()
       diff.compare(corrected_spectrum)



