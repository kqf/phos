#!/usr/bin/python

from spectrum.spectrum import PtAnalyzer, Spectrum
from spectrum.input import Input, TimecutInput

import check_default

class CheckPileup(check_default.CheckDefault):
    def setUp(self):
        super(CheckPileup, self).setUp()
        f = lambda x, y, z: PtAnalyzer(x, label=y, mode=z).quantities()
        self.results = [
                        f(Input('input-data/LHC16k-new.root', 'PhysOnlyTender').read(), 'no timecut', self.mode),
                        f(TimecutInput('input-data/LHC16k-new.root', 'TimeOnlyTender', 'MassPtMainMain').read(), '12.5 ns', self.mode), 
                       ]


if __name__ == '__main__':
    main()