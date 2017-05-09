#!/usr/bin/python

from spectrum.spectrum import Spectrum
from spectrum.input import Input, TimecutInput
from spectrum.sutils import get_canvas, adjust_canvas
from spectrum.options import Options

import unittest

class CheckMC(unittest.TestCase):

    def setUp(self):
        super(CheckMC, self).setUp()
        f = lambda x, y, z: Spectrum(x, label=y, mode = 'q', options = z).evaluate()

        # The problem with the time distribution in MC:
        #  The right flag in AddTender should be used for MC case.

        data =  f(Input('input-data/LHC16.root', 'PhysTender').read(), 'Data', Options())
        pythia = f(TimecutInput('input-data/Pythia-LHC16.root', 'TimeTender', 'MassPtN3').read(), 'Pythia', Options(priority = 0))
        epos =   f(TimecutInput('input-data/EPOS-LHC16.root', 'TimeTender', 'MassPtN3').read(), 'EPOS', Options(priority = 0)) 

        # self.results = [[data, data], [data, data], [data, data]]
        self.results = [[data, pythia], [data, epos], [epos, pythia]]
                       

    def testResultMC(self):
        c1 = get_canvas(1./2, resize=True)

        import spectrum.comparator as cmpr
        for r in self.results:
            diff = cmpr.Comparator()
            diff.compare_set_of_histograms(r)


class CheckMCDifferentVersions(unittest.TestCase):

    def setUp(self):
        super(CheckMCDifferentVersions, self).setUp()
        f = lambda x, y, z: Spectrum(x, label=y, mode = 'q', options = z).evaluate()

        # The problem with the time distribution in MC:
        #  The right flag in AddTender should be used for MC case.

        data = f(Input('input-data/LHC16.root', 'PhysTender').read(), 'Data', Options())
        new = f(TimecutInput('input-data/Pythia-LHC16.root', 'TimeTender', 'MassPtN3').read(), 'Run2Default', Options(priority = 1))
        old = f(TimecutInput('input-data/Pythia-LHC16-iteration2.root', 'TimeTender', 'MassPtN3').read(), 'LHC16all', Options(priority = 0)) 

        self.results = [new, data, old]
  
    def testResultMC(self):
        c1 = adjust_canvas(get_canvas(1./2, resize = True))

        import spectrum.comparator as cmpr
        diff = cmpr.Comparator()
        diff.compare_set_of_histograms(self.results)




if __name__ == '__main__':
    main()