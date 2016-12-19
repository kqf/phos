import unittest

from optimizer.optimizer import Optimizer
from optimizer.metrics import MaximumSignalMetrics, MetricInput, MaximumDeviationMetrics
import ROOT

class TimecutOptimizer(unittest.TestCase):

    def setUp(self):
        # This should be done because fitter is a static object.
        ROOT.TVirtualFitter.SetDefaultFitter('Minuit2')

    def Ranges(self):
        inp = MetricInput('input-data/LHC16k-pass1-ok.root', 'TimeTender', 'MassPtTOF')
        for i in [10, 12, 20, 25, 50, 100]:
            inp.project(i * 1e-9, True)

    def ktestCutMaxSignal(self):
        inp = MetricInput('input-data/LHC16k-pass1-ok.root', 'TimeTender', 'MassPtTOF')
        opt = Optimizer(MaximumSignalMetrics(inp))
        opt.minimize()

    def testCutMaxRatio(self):
        ref = MetricInput('input-data/LHC16k-pass1-ok.root', 'PhysTender', 'MassPtN3')
        inp = MetricInput('input-data/LHC16k-pass1-ok.root', 'TimeTender', 'MassPtTOF')
        opt = Optimizer(MaximumDeviationMetrics(inp, ref))
        opt.minimize()




