from spectrum.comparator import Comparator
from spectrum.broot import BROOT as br

import ROOT
import unittest

from test.systematics.genergy_scale import TestGlobalEnergyScaleUncetanity
from test.systematics.nonlinearity_scan import NonlinearityParameters

class DrawAllSources(unittest.TestCase):

	def test_all(self):
		tests = NonlinearityParameters(), TestGlobalEnergyScaleUncetanity()
		output = [test.test_systematics() for test in tests]

		diff = Comparator()
		diff.compare(output)


