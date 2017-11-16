import unittest

from spectrum.spectrum import CompositeSpectrum
from spectrum.comparator import Comparator
from spectrum.broot import BROOT as br
from spectrum.input import Input


class TestCompositeSpectrum(unittest.TestCase):


   def test_interface(self):
        datadir = '/single/weight2/'
        inputs = {
            Input(datadir + 'LHC17j3b1', 'PhysEffOnlyTender'): (0, 7), 
            Input(datadir + 'LHC17j3b2', 'PhysEffOnlyTender'): (7, 20)
        }

        spectrum_estimator = CompositeSpectrum(inputs)
        for est in spectrum_estimator.spectrums:
            pass
            # est.opt.show_img = True
            # est.analyzer.opt.show_img = True

        histograms = spectrum_estimator.evaluate()

        # TODO: Should I draw this in discover mode?
        diff = Comparator()
        for hist in histograms:
            diff.compare(hist)
   