#!/usr/bin/python

from spectrum.spectrum import PtAnalyzer, Spectrum
from spectrum.input import Input, TimecutInput

from phspace import InclusiveGenerator

import test.check_default
import os

class CheckPileup(test.check_default.CheckDefault):
    def setUp(self):
        super(CheckPileup, self).setUp()

        self.genfilename = 'LHC16-fake.root'
        generator = InclusiveGenerator('input-data/LHC16.root')
        generator.save_fake(self.genfilename)

        f = lambda x, y, z: Spectrum(x, label=y, mode=z, relaxedcb=True).evaluate()
        self.results = [
                        f(Input(self.genfilename, generator.selname).read(), '', self.mode)
                        # generator.real_distributions()
                       ]

    def tearDown(self):
        os.remove(self.genfilename)


if __name__ == '__main__':
    main()