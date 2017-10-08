from spectrum.comparator import Comparator
from spectrum.broot import BROOT as br

import ROOT
import unittest

from test.systematics.yield_extraction import RawYieldError
from test.systematics.nonlinearity_scan import NonlinearityScanner
from test.systematics.genergy_scale import GlobalEnergyScaleUncetanityEvaluator

class DrawAllSources(unittest.TestCase):

    def test_all(self):
        stop = False
        tests = RawYieldError(stop), #GlobalEnergyScaleUncetanityEvaluator(stop),# NonlinearityScanner(stop)
        output = [test.test_systematics() for test in tests]

        diff = Comparator()
        diff.compare(output)


