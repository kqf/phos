import unittest
import ROOT

from spectrum.efficiency import Efficiency
from spectrum.comparator import Comparator
from spectrum.broot import BROOT as br
from test.mc.single.efficiency import FitEfficiency
from vault.datavault import DataVault


def eff_function():
    func_eff = ROOT.TF1("func_efficiency", "[2] * (1.+[0]*TMath::Exp(-x/2*x/2/2./[1]/[1]))", 0, 100);
    func_eff.SetParNames('A', '#sigma', 'E_{scale}')
    func_eff.SetParameter(0, -0.05)
    func_eff.SetParameter(1, 0.6)
    func_eff.SetParameter(2, 1.04)
    return func_eff

class TestEfficiencyPi0(unittest.TestCase):

    def test_eff_overlap(self):
    	func_eff = eff_function()
        files = {
            DataVault().file("single #eta", "low"): (0, 10),
            DataVault().file("single #eta", "high"): (10, 20)
        }

        estimator = FitEfficiency("#eta", func_eff)
        estimator.estimate(files)