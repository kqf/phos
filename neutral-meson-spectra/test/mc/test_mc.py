#!/usr/bin/python

from spectrum.spectrum import Spectrum
from spectrum.input import Input, TimecutInput
from spectrum.sutils import get_canvas

import test.check_default

class CheckMC(test.check_default.CheckDefault):

    def setUp(self):
        super(CheckPileup, self).setUp()
        f = lambda x, y, z: Spectrum(x, label=y, mode=z, relaxedcb=True).evaluate()

        # TODO: Investigate the problem with the time distribution in MC.
        #

        self.results = [
                        f(Input('input-data/LHC16.root', 'PhysTender').read(), '12.5 ns', self.mode),
                        f(TimecutInput('input-data/LHC16-MC-pythia.root', 'QualTender', 'MassPtN3').read(), 'no timecut', self.mode)
                       ]
                       
        canvas = get_canvas(1. / 2.)


if __name__ == '__main__':
    main()