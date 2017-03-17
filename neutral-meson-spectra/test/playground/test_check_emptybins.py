#!/usr/bin/python

from spectrum.spectrum import Spectrum
from spectrum.input import Input
import test.check_default

class CheckEmptyBins(test.check_default.CheckDefault):
    
    def test(self):
        f = lambda x, y, z: Spectrum(x, label=y, mode=z, relaxedcb=True).evaluate()

        # TODO: add option handler for such cases
        self.results = [
                        f(Input('input-data/LHC16.root', 'PhysTender').read(), 'average', self.mode),
                        f(Input('input-data/LHC16.root', 'PhysTender').read(), 'noempty', self.mode)
                       ]


if __name__ == '__main__':
    main()