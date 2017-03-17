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
        self.generator = InclusiveGenerator('input-data/LHC16.root', 'config/test_algorithm.json')

    
    def test(self):
        f = lambda x, y, z: Spectrum(x, label=y, mode=z, relaxedcb=True).evaluate()
        self.original_distributions = self.generator.generate(100000)
        self.generator.save_fake(self.genfilename)
        self.results = [
                        [f(Input(self.genfilename, self.generator.selname).read(), '', self.mode)[2]],
                        [self.original_distributions]
                       ]


    def tearDown(self):
        super(CheckAlgorithm, self).tearDown()
        os.remove(self.genfilename)


if __name__ == '__main__':
    main()