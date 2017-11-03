import unittest

from spectrum.nonlinearity import Nonlinearity
from spectrum.comparator import Comparator
from spectrum.broot import BROOT as br


class TestNonlinearity(unittest.TestCase):

    @unittest.skip('')
    def test_interface(self):
        efficiency_estimator = Efficiency('hPt_#pi^{0}_primary_', 'eff', 'Pythia-LHC16-a5')
        efficiency = efficiency_estimator.eff()
        efficiency.SetTitle('Testing the interface')

        diff = Comparator()
        diff.compare(efficiency)

        
        efficiency_estimator = Efficiency('hPt_#pi^{0}_primary_', 'eff', 'Pythia-LHC16-a5')
        efficiency = efficiency_estimator.eff()
        efficiency.SetTitle('Testing the interface')

        diff = Comparator()
        diff.compare(efficiency)


    def _nonlinearity_function(self):
        func_nonlin = ROOT.TF1("func_nonlin", "[2] * (1.+[0]*TMath::Exp(-x/2*x/2/2./[1]/[1]))", 0, 100);
        func_nonlin.SetParNames('A', '#sigma', 'E_{scale}')
        func_nonlin.SetParameter(0, -0.05)
        func_nonlin.SetParameter(1, 0.6)
        func_nonlin.SetParLimits(1, 0, 10)
        func_nonlin.SetParameter(2, 1.04)
        return func_nonlin


    @unittest.skip('')
    def test_nonlin_general(self):
        """
            Estimates nonlinearity parameters for General purpose MC
        """
        mc = Spectrum(Input('Pythia-LHC16-a5', 'PhysRawOnlyTender'), Options('R2D zs 20 MeV nonlin', 'd'))
        mc = mc.evaluate()
        mc = mc.mass
        func = self._nonlinearity_function()
        nonlin = Nonlinearity(self.data, mc, func, mcname = 'pythia8')
        nonlin.evaluate_parameters()

  