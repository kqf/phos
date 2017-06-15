#!/usr/bin/python

from spectrum.spectrum import Spectrum
from spectrum.input import Input
from spectrum.options import Options
from spectrum.ptanalyzer import PtDependent

from phspace import InclusiveGenerator

import test.check_default
import os

class CheckAlgorithm(test.check_default.CheckDefault):
    def setUp(self):
        super(CheckAlgorithm, self).setUp()

        self.genfilename = 'LHC16-fake.root'
        self.generator = InclusiveGenerator('input-data/Pythia-LHC16-iteration18.root', 'config/test_algorithm.json', genfilename = self.genfilename, flat = True)
        self.clean = False

    
    def test(self):
        f = lambda x, y, z: Spectrum(x, label=y, mode=z, options=Options(relaxedcb=False)).evaluate()
        self.original_distributions = self.generator.generate(10000)
        
        PtDependent.divide_bin_width(self.original_distributions)
        self.original_distributions.priority = 1
        self.original_distributions.logy = 1

        reconstructed = f(Input(self.genfilename, self.generator.selname).read(), '', self.mode)[4]
        PtDependent.divide_bin_width(reconstructed)

        self.results = [
                        [reconstructed],
                        [self.original_distributions]
                       ]



    def tearDown(self):
        super(CheckAlgorithm, self).tearDown()
        if self.clean:
            os.remove(self.genfilename)
