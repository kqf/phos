from spectrum.spectrum import Spectrum, CompositeSpectrum
from spectrum.input import Input
from spectrum.options import Options
from spectrum.broot import BROOT as br
import spectrum.comparator as cmpr

import unittest
import operator


class TestMassWidth(unittest.TestCase):


    def setUp(self):
        self.results = []
        datadir = '/single/weight2/'
        self.shape_inputs = {
            Input(datadir + 'LHC17j3b1', 'PhysEffOnlyTender'): (0, 7), 
            Input(datadir + 'LHC17j3b2', 'PhysEffOnlyTender'): (7, 20)
        }


    @unittest.skip('')
    def test_different_mc_productions(self):
        masses, widths = zip(*self.results)[0:2]

        diff = cmpr.Comparator((0.5, 1.), rrange = (0, 2),
                        crange=(0.1, 0.15), oname = 'compared-spmc-masses')
        diff.compare(masses)

        diff = cmpr.Comparator((0.5, 1.), rrange = (0, 2),
                        crange=(0.0, 0.02), oname = 'compared-spmc-widths')
        diff.compare(widths)


    def test_spectrum_shape(self):
        spectrum_estimator = CompositeSpectrum(self.shape_inputs)
        spmc = spectrum_estimator.evaluate()
        br.scalew(spmc.spectrum, 1. / spmc.spectrum.Integral())
        spmc.spectrum.label = 'mc'

        dinp, dopt = Input('LHC16', 'PhysOnlyTender', label='data'), Options('d')
        data = Spectrum(dinp, dopt).evaluate()
        br.scalew(data.spectrum, 1. / data.spectrum.Integral())

        diff = cmpr.Comparator()
        diff.compare(data.spectrum, spmc.spectrum)