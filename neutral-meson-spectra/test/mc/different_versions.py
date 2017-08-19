#!/usr/bin/python

from spectrum.spectrum import Spectrum
from spectrum.input import Input, TimecutInput
from spectrum.sutils import get_canvas, adjust_canvas
from spectrum.options import Options

import unittest
import operator


class CheckMCDifferentVersions(unittest.TestCase):

    def setUp(self):
        inputs = Input('LHC16', 'PhysOnlyTender'), Input('Pythia-LHC16-a5', 'PhysNonlinTender'),\
             Input('Pythia-LHC16-a5', 'PhysNonlinTender')

        inputs = map(operator.methodcaller('read'), inputs)
        options = Options('Data', 'q'), Options('Pythia8', 'q', priority = 1), Options('EPOS', 'q', priority = 1)

        f = lambda x, y: Spectrum(x, y).evaluate()
        self.results = map(f, inputs, options)


    def testResultMC(self):
        c1 = adjust_canvas(get_canvas(1., resize = True))

        import spectrum.comparator as cmpr
        diff = cmpr.Comparator((1., 1.))
        diff.compare_set_of_histograms(self.results)

        c1 = adjust_canvas(get_canvas(1., resize = True))
        masses, widths = zip(*self.results)[0:2]
        diff.compare_multiple_ratios(widths, masses)


if __name__ == '__main__':
    main()