#!/usr/bin/python

from spectrum.spectrum import Spectrum
from spectrum.input import Input
from spectrum.options import Options
from spectrum.sutils import gcanvas, adjust_canvas

import test.check_default
import unittest

def run_analysis(opt, infile, selection):
    def f(x, y): 
        x.label = y
        return Spectrum(x, opt).evaluate()

    results = map(f, *Input(infile, selection, 'MassPt').read_per_module())
    return results

class CheckModules(test.check_default.CheckDefault):

    def testPi0(self):
        opt = Options(mode='d')
        opt.pt.config = 'config/test_different_modules.json'
        self.results = run_analysis(opt, 'input-data/LHC16.root', 'PhysTender')
        self.c1 = adjust_canvas(gcanvas())

    def testEta(self):
        opt = Options(particle='eta', mode='d')
        opt.pt.config = 'config/test_different_modules.json'
        self.results = run_analysis(opt, 'input-data/LHC16.root', 'EtaTender')
        self.c1 = adjust_canvas(gcanvas())



if __name__ == '__main__':
    main()