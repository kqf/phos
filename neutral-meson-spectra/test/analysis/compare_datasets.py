import unittest

from spectrum.options import Options
from spectrum.spectrum import Spectrum
from spectrum.comparator import Comparator
from spectrum.broot import BROOT as br

from vault.datavault import DataVault

# TODO: Use parallel pipeline
def compare_for_particle(particle):
    new_data = Spectrum(
        DataVault().input("data", "LHC17 qa1"),
        Options(particle)
    )

    old_data = Spectrum(
        DataVault().input("data"),
        Options(particle)
    )

    diff = Comparator()
    for hist1, hist2 in zip(new_data.evaluate("2017"), old_data.evaluate("2016")):
        if 'spectrum' in hist1.GetName():
            br.scalew(hist1)
            br.scalew(hist2)
        diff.compare(hist1, hist2)


class TestCompareDatasets(unittest.TestCase):

    def test_gives_similar_results_for_pions(self):
        compare_for_particle("#pi^{0}")

    def test_gives_similar_results_for_eta(self):
        compare_for_particle("#eta")
