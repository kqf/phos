import unittest

from spectrum.efficiency import Efficiency, EfficiencyMultirange
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
    


class TestMultirangeEfficiency(unittest.TestCase):

    def test_interface(self):
        efficiency_estimator = EfficiencyMultirange('hPt_#pi^{0}_primary_', 'eff', {'LHC17j3b1': (0, 7), 'LHC17j3b2': (7, 20)})
        efficiency = efficiency_estimator.eff()
        efficiency.SetTitle('Testing the interface')

        diff = Comparator()
        diff.compare(efficiency)
        

  