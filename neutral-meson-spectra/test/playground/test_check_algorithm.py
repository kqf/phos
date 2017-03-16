#!/usr/bin/python

from spectrum.spectrum import Spectrum
from spectrum.input import Input

from phspace import InclusiveGenerator

import test.check_default
import os

class CheckAlgorithm(test.check_default.CheckDefault):
    def setUp(self):
        super(CheckAlgorithm, self).setUp()

        self.genfilename = 'LHC16-fake.root'
        self.generator = InclusiveGenerator('input-data/LHC16.root')
        self.original_distributions = self.generator.save_fake(self.genfilename)

    
    def test(self):
        f = lambda x, y, z: Spectrum(x, label=y, mode=z, relaxedcb=True).evaluate()
        self.results = [
                        f(Input(self.genfilename, self.generator.selname).read(), '', self.mode),
                        self.original_distributions
                       ]
  
    def tearDown(self):
        os.remove(self.genfilename)


if __name__ == '__main__':
    main()