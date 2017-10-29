import unittest

from spectrum.spectrum import CompositeSpectrum
from spectrum.comparator import Comparator
from spectrum.broot import BROOT as br
from spectrum.input import Input


class TestCompositeSpectrum(unittest.TestCase):


   def test_interface(self):
        inputs = {Input('LHC17j3b1'): (0, 7), Input('LHC17j3b2'): (7, 20)}
        spectrum_estimator = CompositeSpectrum(inputs)
        histograms = spectrum_estimator.evaluate()
        
        diff = Comparator()
        diff.compare(histograms)
   