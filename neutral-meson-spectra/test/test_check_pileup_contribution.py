#!/usr/bin/python

from spectrum.spectrum import PtAnalyzer, Spectrum
from spectrum.input import Input, TimecutInput

import check_default

class CheckPileup(check_default.CheckDefault):
    def setUp(self):
        super(CheckPileup, self).setUp()
        f = lambda x, y, z: Spectrum(x, label=y, mode=z, relaxedcb=True).evaluate()
        # TODO: figure out what is wrong with this histogram
        # MassPtMainMain 
        self.results = [
                        f(TimecutInput('input-data/LHC16.root', 'TimeTender', 'MassPtN3').read(), 'no timecut', self.mode), 
                        f(Input('input-data/LHC16.root', 'PhysTender').read(), '12.5 ns', self.mode)
                       ]


if __name__ == '__main__':
    main()