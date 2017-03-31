import unittest

from spectrum.sutils import get_canvas, wait
from optimizer.optimizer import Optimizer
from optimizer.metrics import MaximumSignalMetrics, MetricInput, MaximumDeviationMetrics
import ROOT

def process(data, pref):
    c1 = get_canvas()
    c1.Divide(2, 1)
    for i, h in enumerate(data):
        c1.cd(i + 1)
        c1.SetLogz()
        h.SetTitle(h.GetTitle() + pref[i])
        h.GetYaxis().SetTitle('Asymmetry')
        h.Draw('colz')
    wait('name', True, False)

class TimecutOptimizer(unittest.TestCase):

    def setUp(self):
        # This should be done because fitter is a static object.
        ROOT.TVirtualFitter.SetDefaultFitter('Minuit2')
        self.canvas = get_canvas()

    @unittest.skip('Temporary skiping the test')
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

    def testAsymmetryDependence(self):
        ROOT.gStyle.SetOptStat('e')
        inp = MetricInput('input-data/LHC16-new.root', 'QualTender', 'MassPtN3A')

        data_m = map(lambda x: x.Project3D("zx"), [inp.data, inp.mixing])
        process(data_m, ['', 'mixing'])

        data_pt = map(lambda x: x.Project3D("zy"), [inp.data, inp.mixing])
        process(data_, ['', 'mixing'])


    # def testCutMaxSignal(self):
    #     inp = MetricInput('input-data/LHC16k-pass1.root', 'TimeTender', 'MassPtTOF')
    #     opt = Optimizer(MaximumSignalMetrics(inp))
    #     opt.minimize()

    # def rtestCutMaxRatio(self):
    #     ref = MetricInput('input-data/LHC16k-pass1-ok.root', 'PhysTender', 'MassPtN3')
    #     inp = MetricInput('input-data/LHC16k-pass1-ok.root', 'TimeTender', 'MassPtTOF')
    #     opt = Optimizer(MaximumDeviationMetrics(inp, ref))
    #     opt.minimize()




