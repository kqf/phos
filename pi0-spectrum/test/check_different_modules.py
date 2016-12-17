#!/usr/bin/python

import unittest
import ROOT

from spectrum.spectrum import PtAnalyzer, Spectrum
from spectrum.input import Input

class CheckModules(unittest.TestCase):

	def setUp(self):
	    self.canvas = ROOT.TCanvas('c1', 'Canvas', 1000, 500)

	def testModules(self):
	    # f = lambda x, y, z: Spectrum(x, label=y, mode=z).evaluate()
	    f = lambda x, y: PtAnalyzer(x, label=y, mode='q').quantities()

	    results = map(f, *Input('input-data/LHC16k-MyTask.root', 'PhysTender', 'MassPt').read_per_module())

	    import spectrum.comparator as cmpr
	    diff = cmpr.Comparator()
	    diff.compare_set_of_histograms(results)


if __name__ == '__main__':
    main()