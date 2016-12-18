import unittest

from optimizer.optimizer import Optimizer
from optimizer.metrics import Metrics, MetricInput
from spectrum.spectrum import PtAnalyzer, Spectrum
import ROOT

class TimecutOptimizer(unittest.TestCase):

    def setUp(self):
        # This should be done because fitter is a static object.
        ROOT.TVirtualFitter.SetDefaultFitter('Minuit2')

    def Ranges(self):
        inp = Input('input-data/LHC16k-pass1-ok.root', 'MassPtTOF')
        for i in [10, 12, 20, 25, 50, 100]:
            inp.project(i * 1e-9, True)

    def testCut(self):
        # inp = OptimizerInput('input-data/LHC16k-pass1-ok.root', 'TimeTender', 'MassPtTOF')
        opt = Optimizer(Metrics())
        opt.minimize()



