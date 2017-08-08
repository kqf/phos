#!/usr/bin/python

from spectrum.spectrum import Spectrum
from spectrum.input import Input, TimecutInput
from spectrum.sutils import get_canvas, adjust_canvas
from spectrum.options import Options

import unittest

# This test is just to compare peak position mass and spectrum
# for different productions in MC and Data
#

class CompareDataMC(unittest.TestCase):

    def setUp(self):
        super(CheckMC, self).setUp()
        f = lambda x, y, z: Spectrum(x, label=y, mode = 'q', options = z).evaluate()


        data   = f(Input('input-data/LHC16.root', 'PhysTender').read(), 'Data', Options())
        pythia = f(Input('input-data/Pythia-LHC16-a1.root', 'PhysNonlinTender', 'MassPt').read(), 'Pythia', Options(priority = 0))
        epos   = f(Input('input-data/EPOS-LHC16.root', 'PhysNonlinTender', 'MassPt').read(), 'EPOS', Options(priority = 0)) 

        # self.results = pythia
        self.results = [[data, pythia], [data, epos], [epos, pythia]]
                       

    def testResultMC(self):
        c1 = get_canvas(1./2, resize=True)

        import spectrum.comparator as cmpr
        for r in self.results:
            diff = cmpr.Comparator()
            diff.compare(r)

