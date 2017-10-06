import unittest

# from spectrum.spectrum import Spectrum 
from spectrum.input import Input 
from spectrum.options import Options 
from spectrum.efficiency import Efficiency
from spectrum.corrected_yield import CorrectedYield

from spectrum.comparator import Comparator


class TestCorrectedYield(unittest.TestCase):

    def test_interface(self):
        inp, opt = Input('LHC16.root', 'PhysOnlyTender'), Options('data', 'q')
        eff = Efficiency('hPt_#pi^{0}_primary_', 'eff', 'Pythia-LHC16-a5').eff()
        cy_estimator = CorrectedYield(inp, opt, eff)

        corrected_spectrum1 = cy_estimator.evaluate()

        corrected_spectrum2 = CorrectedYield.create_evaluate('LHC16.root',\
                 'PhysOnlyTender', 'Pythia-LHC16-a5', 'hPt_#pi^{0}_primary_')

        diff = Comparator()
        diff.compare(corrected_spectrum1,
            corrected_spectrum2)
        

