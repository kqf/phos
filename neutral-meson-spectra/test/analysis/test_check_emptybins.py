#!/usr/bin/python

from vault.datavault import DataVault
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
        arguments = []
        for l, average in {'func': {}, 'empty': {'empty'}}.iteritems():
            option = Options()
            option.invmass.average = average
            sinput = Input(
                DataVault().file("data"), 
                'PhysTender',
                label=l
            )
            arguments.append((sinput, option))

        self.results = [Spectrum(*args).evaluate() for args in arguments]


if __name__ == '__main__':
    main()