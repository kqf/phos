import unittest
import ROOT

from spectrum.spectrum import Spectrum
# from spectrum.nonlinearity import Nonlinearity
from vault.datavault import DataVault
from spectrum.options import NonlinearityOptions
from spectrum.efficiency import Nonlinearity


def nonlinearity_function():
    func_nonlin = ROOT.TF1(
        "func_nonlin",
        "[2] * (1.+[0]*TMath::Exp(-x/2*x/2/2./[1]/[1]))",
        0, 100
    )
    func_nonlin.SetParNames('A', '#sigma', 'E_{scale}')
    func_nonlin.SetParameter(0, -0.05)
    func_nonlin.SetParameter(1, 0.6)
    func_nonlin.SetParLimits(1, 0, 10)
    func_nonlin.SetParameter(2, 1.04)
    return func_nonlin


class TestNonlinearityEstimator(unittest.TestCase):

    def test_interace(self):
        options = NonlinearityOptions()
        options.fitf = nonlinearity_function()

        estimator = Nonlinearity(options)
        estimator.transform(
            [
                DataVault().input('data'),
                DataVault().input('pythia8')
            ],
            "Testing the interface"
        )


class TestNonlinearity(unittest.TestCase):

    @unittest.skip('')
    def test_interface(self):
        data = Spectrum(
            DataVault().input('data', 'stable', 'PhysOnlyTender', label='Data')
        )
        data = data.evaluate()
        mc = Spectrum(
            DataVault().input('data', 'stable', label='R2D zs 20 MeV nonlin')
        )
        mc = mc.evaluate()
        func = nonlinearity_function()
        nonlin = Nonlinearity(data.mass, mc.mass, func, mcname='pythia8')
        nonlin.evaluate_parameters()
