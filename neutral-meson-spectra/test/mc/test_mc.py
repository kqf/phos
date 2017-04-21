#!/usr/bin/python

from spectrum.spectrum import Spectrum
from spectrum.input import Input, TimecutInput
from spectrum.sutils import get_canvas

import unittest

class CheckMC(unittest.TestCase):

    def setUp(self):
        super(CheckMC, self).setUp()
        f = lambda x, y: Spectrum(x, label=y, mode = 'q').evaluate()

        # TODO: Investigate the problem with the time distribution in MC.
        #

        # TODO: Fix colors for pythia-epos case.
        #

        data =  f(Input('input-data/LHC16.root', 'PhysTender').read(), 'Data')
        pythia = f(TimecutInput('input-data/Pythia-LHC16.root', 'TimeTender', 'MassPtN3').read(), 'Pythia')
        epos =   f(TimecutInput('input-data/EPOS-LHC16.root', 'TimeTender', 'MassPtN3').read(), 'EPOS') 

        # self.results = [[data, data], [data, data], [data, data]]
        self.results = [[data, pythia], [data, epos], [epos, pythia]]
                       

    def testResultMC(self):
        c1 = get_canvas(1./2, resize=True)

        import spectrum.comparator as cmpr
        for r in self.results:
            diff = cmpr.Comparator()
            diff.compare_set_of_histograms(r)




if __name__ == '__main__':
    main()