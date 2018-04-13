import unittest
import ROOT

from spectrum.spectrum import Spectrum
from spectrum.options import Options
from spectrum.input import Input
from spectrum.nonlinearity import Nonlinearity
from spectrum.comparator import Comparator
from spectrum.broot import BROOT as br

from vault.datavault import DataVault

class TestNonlinearity(unittest.TestCase):

    # @unittest.skip('')
    def test_interface(self):
        data = Spectrum(
            DataVault().input('data', 'stable'), 'PhysOnlyTender', label='Data')
        )
        data = data.evaluate()
        mc = Spectrum(
            DataVault().input('data', 'stable'), label='R2D zs 20 MeV nonlin')
        )
        mc = mc.evaluate()
        func = self._nonlinearity_function()
        nonlin = Nonlinearity(data.mass, mc.mass, func, mcname = 'pythia8')
        nonlin.evaluate_parameters()


    def _nonlinearity_function(self):
        func_nonlin = ROOT.TF1("func_nonlin", "[2] * (1.+[0]*TMath::Exp(-x/2*x/2/2./[1]/[1]))", 0, 100);
        func_nonlin.SetParNames('A', '#sigma', 'E_{scale}')
        func_nonlin.SetParameter(0, -0.05)
        func_nonlin.SetParameter(1, 0.6)
        func_nonlin.SetParLimits(1, 0, 10)
        func_nonlin.SetParameter(2, 1.04)
        return func_nonlin


