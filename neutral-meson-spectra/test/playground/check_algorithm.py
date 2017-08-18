#!/usr/bin/python

from spectrum.spectrum import Spectrum
from spectrum.options import Options
from spectrum.sutils import scalew
from spectrum.input import Input

from test.playground.phspace import InclusiveGenerator

import os
import test.check_default


class CheckAlgorithm(test.check_default.CheckDefault):
    def setUp(self):
        super(CheckAlgorithm, self).setUp()

        self.mode = 'd'
        self.genfilename = 'LHC16-fake.root'
        infile, conf = 'input-data/LHC16.root', 'config/test_algorithm.json'
        self.generator = InclusiveGenerator(infile, conf, genfilename = self.genfilename, flat = True)
        self.clean = False



    def test(self):
        f = lambda x, y, z: Spectrum(x, options=Options(y, z)).evaluate()
        generated = self.generator.generate(100000)
        generated.logy = 1
        generated.priority = 1

        reconstructed = f(Input(self.genfilename, self.generator.selname), 'reconstructed', self.mode).npi0


        self.results = map(scalew, [reconstructed, generated])



    def tearDown(self):
        super(CheckAlgorithm, self).tearDown()
        if self.clean:
            os.remove(self.genfilename)
