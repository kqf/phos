#!/usr/bin/python

from spectrum.spectrum import Spectrum
from spectrum.input import Input
from spectrum.options import Options
from spectrum.sutils import get_canvas, adjust_canvas

import test.check_default
import unittest


class CheckModules(test.check_default.CheckDefault):

    def run_analysis(self, opt, selection):
        f = lambda x, y: Spectrum(x, label=y, mode=self.mode, options=opt).evaluate()
        self.results = map(f, *Input('input-data/LHC16.root', 'PhysTender', 'MassPt').read_per_module())
        self.c1 = adjust_canvas(get_canvas())

    def testPi0(self):
        opt = Options(ptconfig='config/test_different_modules.json')
        self.run_analysis(opt, 'PhysTender')

    # @unittest.skip('test')
    def testEta(self):
        opt = Options(particle='eta', ptconfig='config/test_different_modules.json')
        self.run_analysis(opt, 'EtaTender')



if __name__ == '__main__':
    main()