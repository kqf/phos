#!/usr/bin/python

from spectrum.spectrum import Spectrum
from spectrum.input import Input
from spectrum.options import Options
from spectrum.broot import BROOT as br
import spectrum.comparator as cmpr

import unittest
import operator


class TestMassWidth(unittest.TestCase):

    def setUp(self):
        ddir = '/single/weight0/'
        inputs = (Input(ddir + 'LHC17j3b1', 'PhysEffOnlyTender'),
                  Input(ddir + 'LHC17j3b2', 'PhysEffOnlyTender'))


        inputs = map(operator.methodcaller('read'), inputs)

        # NB: Always set use_mixed to False
        # 

        options = ( Options('low p_{T}', 'q', use_mixed = False), 
                    Options('high p_{T}', 'q', use_mixed = False))
        for opt in options:
            opt.param.fit_range = (0.1, 0.2)

        f = lambda x, y: Spectrum(x, y).evaluate()
        self.results = map(f, inputs, options)



    def test_different_mc_productions(self):
        masses, widths = zip(*self.results)[0:2]

        diff = cmpr.Comparator((0.5, 1.), rrange = (0, 2),
                        crange=(0.1, 0.15), oname = 'compared-spmc-masses')
        diff.compare(masses)

        diff = cmpr.Comparator((0.5, 1.), rrange = (0, 2),
                        crange=(0.0, 0.02), oname = 'compared-spmc-widths')
        diff.compare(widths)



if __name__ == '__main__':
    main()