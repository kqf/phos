import unittest

from spectrum.efficiency import Efficiency
from spectrum.comparator import Comparator
from spectrum.broot import BROOT as br


class TestEfficiency(unittest.TestCase):

    def test_interface(self):
        efficiency_estimator = Efficiency('hPt_#pi^{0}_primary_', 'eff', 'Pythia-LHC16-a5')
        efficiency = efficiency_estimator.eff()
        efficiency.SetTitle('Testing the interface')

        diff = Comparator()
        diff.compare(efficiency)
        

    def test_true_spectrum(self):
        efficiency_estimator = Efficiency('hPt_#pi^{0}_primary_', 'eff', 'Pythia-LHC16-a5')
        true = efficiency_estimator.true()
        true.SetTitle('Testing the denominator')

        diff = Comparator()
        diff.compare(true)


    def test_force_recalculate(self):

        efficiency_estimator = Efficiency('hPt_#pi^{0}_primary_', 'eff', 'Pythia-LHC16-a5')
        efficiency = efficiency_estimator.eff()
        efficiency.SetTitle('Force recarculate')

        diff = Comparator()
        diff.compare(efficiency)
    
