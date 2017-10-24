#!/usr/bin/python

from spectrum.spectrum import Spectrum
from spectrum.input import Input, TimecutInput
from spectrum.sutils import gcanvas, adjust_canvas
from spectrum.options import Options
from spectrum.broot import BROOT as br

import unittest
import operator


class CheckMCDifferentVersions(unittest.TestCase):

    def setUp(self):
        inputs = (
                      Input('LHC16', 'PhysOnlyTender'), Input('Pythia-LHC16-a5', 'PhysNonlinOnlyTender'),\
                      Input('LHC17d20a', 'PhysNonlinOnlyTender'), \
                      # Input('pythia-jet-jet', 'PhysNonlinOnlyTender'), \
                      Input('scaled-LHC17j3b', 'MCStudyTender')
                  )



        inputs = map(operator.methodcaller('read'), inputs)
        options = (
                    Options('Data', 'q', priority = 999), Options('Pythia8', 'q', priority = 1), \
                    Options('EPOS', 'q', priority = 99), \
                    # Options('Pythia8 JJ', 'q', priority = 1), \
                    Options('single', 'q', priority = 99)
                 )


        f = lambda x, y: Spectrum(x, y).evaluate()
        self.results = map(f, inputs, options)


    def testResultMC(self):
        import spectrum.comparator as cmpr
        diff = cmpr.Comparator((1., 1.))
        diff.compare(self.results)

        masses, widths = zip(*self.results)[0:2]

        diff = cmpr.Comparator((0.5, 1.), oname = 'compared-mc-masses')
        diff.compare(masses)

        diff = cmpr.Comparator((0.5, 1.), oname = 'compared-mc-widths')
        diff.compare(widths)

        diff = cmpr.Comparator((1., 1.))
        diff.compare_multiple_ratios(widths, masses)

        c1 = adjust_canvas(gcanvas(1, resize = True))
        spectrums = zip(*self.results)[2]

        for s in spectrums:
            br.scalew(s, 1./s.Integral())

        diff = cmpr.Comparator((1., 1.), oname = 'compared-mc-spectrums')
        diff.compare(spectrums)




if __name__ == '__main__':
    main()