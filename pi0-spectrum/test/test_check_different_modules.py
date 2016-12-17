#!/usr/bin/python

from spectrum.spectrum import PtAnalyzer, Spectrum
from spectrum.input import Input

import check_default
class CheckModules(check_default.CheckDefault):

    def setUp(self):
        super(CheckModules, self).setUp()
        # f = lambda x, y, z: Spectrum(x, label=y, mode=z).evaluate()
        f = lambda x, y: PtAnalyzer(x, label=y, mode=self.mode).quantities()
        self.results = map(f, *Input('input-data/LHC16k-MyTask.root', 'PhysTender', 'MassPt').read_per_module())


if __name__ == '__main__':
    main()