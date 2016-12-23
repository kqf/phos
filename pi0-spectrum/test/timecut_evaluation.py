import unittest

from spectrum.sutils import get_canvas, wait
from optimizer.metrics import MaximumSignalMetrics, MetricInput, MaximumDeviationMetrics
import ROOT

import numpy as np

class Evaluator(object):
    def __init__(self, original, withcut):
        super(Evaluator, self).__init__()
        self.original = original
        self.withcut = withcut

    def cut_characteristic(self):
        eff = ROOT.TGraph()
        for i, (x, y) in enumerate(self.characteristic(self.efficiency)):
            eff.SetPoint(i, x, y)
        eff.Draw('apl')

        # The same for purity
        purity = ROOT.TGraph()
        for i, (x, y) in enumerate(self.characteristic(self.purity)):
            purity.SetPoint(i, x, y)
        purity.Draw('apl same')
        wait('', True)

    def characteristic(self, f):
        cuts = np.linspace(10, 30, 10)
        values = map(f, cuts)
        return zip(cuts, values)

    def efficiency(self, x):
        return (x/ 30.) ** 0.5

    def purity(self, x):
        return (x/30.) ** 2.1


class TestTimecutQuality(unittest.TestCase):

    def setUp(self):
        # This should be done because fitter is a static object.
        ROOT.TVirtualFitter.SetDefaultFitter('Minuit2')
        self.canvas = get_canvas()

    def testEfficiencyVsPurity(self):
        ref = MetricInput('input-data/LHC16k-pass1-ok.root', 'PhysTender', 'MassPtN3')
        inp = MetricInput('input-data/LHC16k-pass1-ok.root', 'TimeTender', 'MassPtTOF')
        ev = Evaluator(inp, ref)
        ev.cut_characteristic()




