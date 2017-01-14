#!/usr/bin/python

from spectrum.spectrum import PtAnalyzer, Spectrum
from spectrum.input import Input, TimecutInput
from test.test_check_different_modules import ModuleAnalyzer

import check_default

# This macro checks parametrization of pi0 mass position and pi0 peak width
# Just compare two different methods of extracting raw yield

class CheckParametrization(check_default.CheckDefault):
    def setUp(self):
        super(CheckParametrization, self).setUp()
        g = lambda x, y, z: Spectrum(x, label=y, mode=z).evaluate()
        f = lambda x, y, z: PtAnalyzer(x, label=y, mode=z).quantities()
        self.results = [
                        f(TimecutInput('input-data/LHC16k-pass1.root', 'TimeTender', 'MassPtMainMain').read(), 'no param', self.mode),
                        g(TimecutInput('input-data/LHC16k-pass1.root', 'TimeTender', 'MassPtMainMain').read(), 'param', self.mode)
                       ]


if __name__ == '__main__':
    main()