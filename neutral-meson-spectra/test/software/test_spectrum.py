import unittest

from spectrum.spectrum import CompositeSpectrum
from spectrum.comparator import Comparator
from spectrum.broot import BROOT as br
from spectrum.input import Input


class TestCompositeSpectrum(unittest.TestCase):


   def test_interface(self):
        datadir = '/single/plain/'
        inputs = {
            Input(datadir + 'scaled-LHC17j3b1', 'MCStudyOnlyTender'): (0, 7), 
            Input(datadir + 'scaled-LHC17j3b2', 'MCStudyOnlyTender'): (7, 20)
        }

        spectrum_estimator = CompositeSpectrum(inputs)
        for est in spectrum_estimator.spectrums:
            est.opt.show_img = True
            est.analyzer.opt.show_img = True

        histograms = spectrum_estimator.evaluate()

        # TODO: Should I draw this in discover mode?
        diff = Comparator()
        for hist in histograms:
            diff.compare(hist)
   