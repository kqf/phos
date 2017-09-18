import unittest

from spectrum.broot import BROOT as br
from spectrum.comparator import Comparator

class ComparePublishedResults(unittest.TestCase):


	def setUp(self):
		tdir = 'Table 1'
		hname = 'Hist1D_y1'
		self.hreader = lambda h: br.io.read(h, tdir, hname)

	def test(self):
		infiles = '7.TeV.root', '2.76.TeV.root', '8.TeV.root'
		histograms = map(self.hreader, infiles)

		for name, hist in zip(infiles, histograms):
			label = name.replace('.', ' ')
			label = name.replace('root', '')
			hist.label = label

		diff = Comparator()
		diff.compare(histograms)

