import unittest

from spectrum.sutils import gcanvas
from optimizer.optimizer import Optimizer
from optimizer.metrics import MaximumSignalMetrics, MetricInput, MaximumDeviationMetrics
import ROOT

#TOOD: Fix metric inputs

class TimecutOptimizer(unittest.TestCase):

    def setUp(self):
        # This should be done because fitter is a static object.
        ROOT.TVirtualFitter.SetDefaultFitter('Minuit2')
        self.canvas = gcanvas()

    def Ranges(self):
        inp = MetricInput('input-data/LHC16k-pass1-ok.root', 'TimeTender', 'MassPtTOF')
        for i in [10, 12, 20, 25, 50, 100]:
            inp.project(i * 1e-9, True)

    def testCutMaxSignal(self):
        inp = MetricInput('input-data/LHC16k-pass1.root', 'TimeTender', 'MassPtTOF')
        opt = Optimizer(MaximumSignalMetrics(inp))
        opt.minimize()

    def rtestCutMaxRatio(self):
        ref = MetricInput('input-data/LHC16k-pass1-ok.root', 'PhysTender', 'MassPtN3')
        inp = MetricInput('input-data/LHC16k-pass1-ok.root', 'TimeTender', 'MassPtTOF')
        opt = Optimizer(MaximumDeviationMetrics(inp, ref))
        opt.minimize()




