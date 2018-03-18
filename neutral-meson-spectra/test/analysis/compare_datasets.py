import unittest

from spectrum.spectrum import Spectrum
from spectrum.comparator import Comparator
from spectrum.broot import BROOT as br

from vault.datavault import DataVault

class TestCompareDatasets(unittest.TestCase):


	def test_gives_similar_results(self):
		new_data = Spectrum(
			DataVault().input("data", "LHC17 qa1")
		)

		old_data = Spectrum(
			DataVault().input("data")
		)

		diff = Comparator()
		for hist1, hist2 in zip(new_data.evaluate("2017"), old_data.evaluate("2016")):
			if 'spectrum' in hist1.GetName():
				br.scalew(hist1)
				br.scalew(hist2)
			diff.compare(hist1, hist2)
