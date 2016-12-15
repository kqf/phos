import unittest
from optimizer.optimizer import Optimizer, Input
from spectrum.spectrum import PtAnalyzer, Spectrum
import ROOT

class TimecutOptimizer(unittest.TestCase):

    def setUp(self):
        pass

    # def testRanges(self):
        # inp = Input('input-data/LHC16k-pass1-ok.root', 'MassPtTOF')
        # for i in [10, 12, 20, 25, 50, 100]:
            # inp.project(i * 1e-9, True)


    def testCut(self):
        ROOT.TVirtualFitter.SetDefaultFitter('Minuit2')
        opt = Optimizer('input-data/LHC16k-pass1-ok.root', 'MassPtTOF')



