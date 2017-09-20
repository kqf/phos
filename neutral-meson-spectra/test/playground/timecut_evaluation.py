import sys
import unittest

from spectrum.sutils import gcanvas, wait
from optimizer.metrics import MaximumSignalMetrics, MetricInput, MaximumDeviationMetrics
import ROOT

import numpy as np


# This is code shouldn't be used for real analysis
# This can be used as a template for Asymmetry cut analysis.

class Evaluator(object):
    def __init__(self, original, withcut):
        super(Evaluator, self).__init__()
        self.original = original
        self.withcut = withcut
        self.stop = 'discover' not in sys.argv

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
        wait('', draw = self.stop)

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
        self.canvas = gcanvas()

    def testEfficiencyVsPurity(self):
        ref = MetricInput('input-data/LHC16k-pass1-ok.root', 'PhysTender', 'MassPtN3')
        inp = MetricInput('input-data/LHC16k-pass1-ok.root', 'TimeTender', 'MassPtTOF')
        ev = Evaluator(inp, ref)
        ev.cut_characteristic()




