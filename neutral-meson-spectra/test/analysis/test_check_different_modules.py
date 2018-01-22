#!/usr/bin/python

from spectrum.spectrum import Spectrum
from spectrum.input import Input
from spectrum.options import Options
from spectrum.sutils import gcanvas, adjust_canvas

import test.check_default
import unittest
import operator

def run_analysis(options, infile, selection):

    inputs = Input.read_per_module(
        infile,
        selection,
        'MassPt',
        options
    )

    estimators = map(
        lambda x: Spectrum(x, options),
        inputs
    )


    results = map(
        operator.methodcaller('evaluate'),
        estimators
    )

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