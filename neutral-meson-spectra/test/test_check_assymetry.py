import unittest

from spectrum.sutils import get_canvas, wait
from optimizer.optimizer import Optimizer
from optimizer.metrics import MaximumSignalMetrics, MetricInput, MaximumDeviationMetrics
import ROOT

class TimecutOptimizer(unittest.TestCase):

    def setUp(self):
        # This should be done because fitter is a static object.
        ROOT.TVirtualFitter.SetDefaultFitter('Minuit2')
        self.canvas = get_canvas()

    def testRanges(self):
        inp = MetricInput('input-data/LHC16.root', 'QualTender', 'MassPtN3A')

        scale = lambda a : a.Scale(1. / a.Integral(a.FindBin(0.3), a.FindBin(0.7)))

        assymetries = []
        for i in [0.1, 0.5, 0.9]:
            p = inp.project(i, True)[0].ProjectionX()
            scale(p)
            assymetries.append(p)

        canvas = get_canvas()
        for i, a in enumerate(assymetries):
        	a.SetLineColor(2 * i + 1)
        	a.SetAxisRange(0.3, 0.7, 'X')
        	a.Draw((i > 0) * 'same')
        wait('name', True, False)

        # TODO: increase statistics to improve the performance
        # 		figure out if additional optimization is needed.

    # def testCutMaxSignal(self):
    #     inp = MetricInput('input-data/LHC16k-pass1.root', 'TimeTender', 'MassPtTOF')
    #     opt = Optimizer(MaximumSignalMetrics(inp))
    #     opt.minimize()

    # def rtestCutMaxRatio(self):
    #     ref = MetricInput('input-data/LHC16k-pass1-ok.root', 'PhysTender', 'MassPtN3')
    #     inp = MetricInput('input-data/LHC16k-pass1-ok.root', 'TimeTender', 'MassPtTOF')
    #     opt = Optimizer(MaximumDeviationMetrics(inp, ref))
    #     opt.minimize()




