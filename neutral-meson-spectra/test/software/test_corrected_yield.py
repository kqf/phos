import unittest

# from spectrum.spectrum import Spectrum
from spectrum.input import Input
from spectrum.options import Options
from spectrum.efficiency import Efficiency
from spectrum.corrected_yield import CorrectedYield

from spectrum.comparator import Comparator
from spectrum.broot import BROOT as br
from vault.datavault import DataVault


class TestCorrectedYield(unittest.TestCase):


    def test_interface_simple(self):
        data = [
            DataVault().input("data"),
            DataVault().input("pythia8")
        ]

        estimator = CorrectedYield()
        estimator.transform(data, ("Test corr yield interface", False))

    @unittest.skip('')
    def test_interface(self):
        inp, opt = Input('LHC16.root', 'PhysOnlyTender', 'data'), Options('q')
        eff = Efficiency('hPt_#pi^{0}_primary_', 'eff', 'Pythia-LHC16-a5').eff()
        cy_estimator = CorrectedYield(inp, opt, eff)

        corrected_spectrum1 = cy_estimator.evaluate()

        corrected_spectrum2 = CorrectedYield.create_evaluate('LHC16.root',\
                 'PhysOnlyTender', 'Pythia-LHC16-a5', 'hPt_#pi^{0}_primary_')


        # This method is better as it compares errors as well
        br.diff(corrected_spectrum1, corrected_spectrum2)

        diff = Comparator()
        diff.compare(corrected_spectrum1,
            corrected_spectrum2)


