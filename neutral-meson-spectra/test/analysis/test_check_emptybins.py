#!/usr/bin/python

from spectrum.spectrum import Spectrum
from spectrum.input import Input
from spectrum.options import Options
import test.check_default


# Problem: There are some bins in invariant mass histogram
#          that have no entries for same event data and 
#          nonzero content for mixed event. ROOT fails to calculate
#          the error in that bin for real/mixed ratio!
#           
#          This test compares different solutions
#

class CheckEmptyBins(test.check_default.CheckDefault):
    
    def test(self):
        sinput = Input('input-data/LHC16.root', 'PhysTender').read()
        options = []
        for l, average in {'func': {}, 'empty': {'empty'}}.iteritems():
            option = Options(l)
            option.invmass.average = average
            options.append(option)

        self.results = [Spectrum(sinput, o).evaluate() for o in options]


if __name__ == '__main__':
    main()