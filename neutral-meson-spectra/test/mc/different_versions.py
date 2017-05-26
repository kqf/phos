#!/usr/bin/python

from spectrum.spectrum import Spectrum
from spectrum.input import Input, TimecutInput
from spectrum.sutils import get_canvas, adjust_canvas
from spectrum.options import Options

import unittest


class CheckMCDifferentVersions(unittest.TestCase):

    def setUp(self):
        super(CheckMCDifferentVersions, self).setUp()
        f = lambda x, y, z: Spectrum(x, label=y, mode = 'q', options = z).evaluate()

        # The problem with the time distribution in MC:
        #  The right flag in AddTender should be used for MC case.

        self.results = [
                             f(Input('input-data/LHC16.root', 'PhysOnlyTender').read(), 'Data', Options())
                            ,f(TimecutInput('input-data/Pythia-LHC16-iteration3.root', 'TimeTender', 'MassPtN3').read(), 'Run2Default', Options(priority = 0)) 
                            ,f(TimecutInput('input-data/Pythia-LHC16-iteration4.root', 'TimeTender', 'MassPtN3').read(), 'R2D zs 20 MeV', Options(priority = 1))
                            # ,f(TimecutInput('input-data/Pythia-LHC16-iteration5.root', 'PhysTender', 'MassPtN3').read(), 'R2D zs 10 MeV', Options(priority = 1))
                            # ,f(TimecutInput('input-data/Pythia-LHC16-iteration8.root', 'PhysTender', 'MassPtN3').read(), 'Nonlinearity', Options(priority = 1))

                            # ,f(TimecutInput('input-data/Pythia-LHC16-iteration2.root', 'TimeTender', 'MassPtN3').read(), 'LHC16all', Options(priority = 0)) 
                            # ,f(TimecutInput('input-data/Pythia-LHC16-iteration7.root', 'PhysTender', 'MassPtN3').read(), 'LHC16 20 MeV', Options(priority = 1))
                            ,f(TimecutInput('input-data/Pythia-LHC16-iteration9.root', 'PhysTender', 'MassPtN3').read(), 'LHC16 25 MeV', Options(priority = 1))
                            # ,f(TimecutInput('input-data/Pythia-LHC16-iteration10.root', 'PhysTender', 'MassPtN3').read(), 'nonlin LHC16 25 MeV', Options(priority = 1))
                            ,f(TimecutInput('input-data/Pythia-LHC16-iteration12.root', 'PhysTender', 'MassPtN3').read(), 'R2D 20 MeV nonlin', Options(priority = 1))
                        ]


  
    def testResultMC(self):
        c1 = adjust_canvas(get_canvas(1./ 2, resize = True))

        import spectrum.comparator as cmpr
        diff = cmpr.Comparator((1./2, 1.))
        diff.compare_set_of_histograms(self.results)

        c1 = adjust_canvas(get_canvas(1., resize = True))
        masses, widths = zip(*self.results)[0:2]
        diff.compare_multiple_ratios(widths, masses)





if __name__ == '__main__':
    main()