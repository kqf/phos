#!/usr/bin/python

from spectrum.spectrum import Spectrum
from spectrum.input import Input
from spectrum.options import Options
from spectrum.sutils import get_canvas, adjust_canvas

import test.check_default
import unittest

def run_analysis(opt, infile, selection):
    f = lambda x, y: Spectrum(x, label=y, mode='d', options=opt).evaluate()
    results = map(f, *Input(infile, selection, 'MassPt').read_per_module())
    return results

class CheckModules(test.check_default.CheckDefault):

    def testPi0(self):
        opt = Options()
        opt.pt.config = 'config/test_different_modules.json'
        self.results = run_analysis(opt, 'input-data/LHC16.root', 'PhysTender')
        self.c1 = adjust_canvas(get_canvas())

    def testEta(self):
        opt = Options(particle='eta')
        opt.pt.config = 'config/test_different_modules.json'
        self.results = run_analysis(opt, 'input-data/LHC16.root', 'EtaTender')
        self.c1 = adjust_canvas(get_canvas())



if __name__ == '__main__':
    main()