import ROOT
import unittest

from vault.formulas import FVault
from spectrum.comparator import Comparator


class TestNonlinearityFunction(unittest.TestCase):

    def test_parameters(self):
        parameters = {
            "recent": [
                1.0644033741013799,
                -0.00847958820741291,
                1.007,
            ],
            "old": [

                -0.014719244288611932,
                2 * 0.8017501954719543,
                1.050000000000015,
            ],
            "plain": [
                0.0,
                2 * 0.8017501954719543,
                1.0,
            ],
            "updated gamma": [
                -0.008502585550404397,
                1.063118454172695,
                1.0222154255076596
            ],
            "updated pi0": [
                -0.022361543707205396,
                1.9834455549215824,
                1.0160704760491277,
            ]

        }

        fv = FVault()
        functions = [
            ROOT.TF1('f' + str(i), fv.func("nonlinearity"), 0, 20)
            for i in parameters
        ]

        histograms = []
        for f, p in zip(functions, parameters):
            f.SetParameters(*parameters[p])
            histograms.append(f.GetHistogram())
            histograms[-1].SetTitle(p)
            histograms[-1].label = p
        Comparator().compare(*histograms)
