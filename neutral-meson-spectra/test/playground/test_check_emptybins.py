#!/usr/bin/python

from spectrum.spectrum import Spectrum
from spectrum.input import Input
from spectrum.options import Options
import test.check_default

class CheckEmptyBins(test.check_default.CheckDefault):
    
    def test(self):
        f = lambda x, y, z, w: Spectrum(x, label=y, mode=z, options=w).evaluate()

        # TODO: add option handler for such cases
        self.results = [
                        f(Input('input-data/LHC16.root', 'PhysTender').read(), 'average', self.mode, Options(average = True)),
                        f(Input('input-data/LHC16.root', 'PhysTender').read(), 'noempty', self.mode, Options(average = False))
                       ]


if __name__ == '__main__':
    main()