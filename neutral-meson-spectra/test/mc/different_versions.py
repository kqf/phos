#!/usr/bin/python

from spectrum.spectrum import Spectrum
from spectrum.input import Input, TimecutInput
from spectrum.sutils import get_canvas, adjust_canvas
from spectrum.options import Options

import unittest


class CheckMCDifferentVersions(unittest.TestCase):

    def setUp(self):
        super(CheckMCDifferentVersions, self).setUp()
        f = lambda x, y, z: Spectrum(x, label=y, mode = 'q', options = z).evaluate()

        # The problem with the time distribution in MC:
        #  The right flag in AddTender should be used for MC case.

        data = f(Input('input-data/LHC16.root', 'PhysOnlyTender').read(), 'Data', Options())
        new = f(TimecutInput('input-data/Pythia-LHC16.root', 'TimeOnlyTender', 'MassPtN3').read(), 'zs 20', Options(priority = 1))
        old = f(TimecutInput('input-data/Pythia-LHC16-iteration3.root', 'TimeOnlyTender', 'MassPtN3').read(), 'zs 12', Options(priority = 0)) 

        print "old", old
        print "new", new
        print "data", data

        self.results = [new, data, old]

  
    def testResultMC(self):
        c1 = adjust_canvas(get_canvas(1./2, resize = True))

        import spectrum.comparator as cmpr
        diff = cmpr.Comparator()
        diff.compare_set_of_histograms(self.results)




if __name__ == '__main__':
    main()