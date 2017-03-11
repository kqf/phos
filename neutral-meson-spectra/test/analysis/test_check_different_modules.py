#!/usr/bin/python

from spectrum.spectrum import PtAnalyzer, Spectrum
from spectrum.input import Input

import test.check_default
import numpy as np


class ModuleAnalyzer(PtAnalyzer):
    def __init__(self, lst, label ='N_{cell} > 3', mode = 'v'):
        super(ModuleAnalyzer, self).__init__(lst, label, mode)

    def divide_into_bins(self):
        nedges = 20
        edges = np.e ** np.linspace(np.log(1.1), np.log(15) , nedges)
        return map(self.hists[0].GetYaxis().FindBin, edges), np.zeros(nedges - 1)


class CheckModules(test.check_default.CheckDefault):

    def setUp(self):
        super(CheckModules, self).setUp()
        # f = lambda x, y, z: Spectrum(x, label=y, mode=z).evaluate()
        f = lambda x, y: ModuleAnalyzer(x, label=y, mode=self.mode).quantities()
        self.results = map(f, *Input('input-data/LHC16.root', 'PhysTender', 'MassPt').read_per_module())



if __name__ == '__main__':
    main()