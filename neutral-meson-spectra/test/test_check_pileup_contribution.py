#!/usr/bin/python

from spectrum.spectrum import PtAnalyzer, Spectrum
from spectrum.input import Input, TimecutInput

import check_default

class CheckPileup(check_default.CheckDefault):
    def setUp(self):
        super(CheckPileup, self).setUp()
        f = lambda x, y, z: Spectrum(x, label=y, mode=z, relaxedcb=True).evaluate()
        # The histogram MassPtMainMain is the same as the histogram MassPtN3 because 
        # timing cut in the TimeTender selection is off
        # Don't forget to enable this cut later
        #

        self.results = [
                        f(TimecutInput('input-data/LHC16.root', 'TimeTender', 'MassPtN3').read(), 'no timecut', self.mode), 
                        f(Input('input-data/LHC16.root', 'PhysTender').read(), '12.5 ns', self.mode)
                       ]


if __name__ == '__main__':
    main()