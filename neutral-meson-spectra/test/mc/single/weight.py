import sys
import unittest

from spectrum.spectrum import Spectrum, CompositeSpectrum
from spectrum.options import Options
from spectrum.input import Input
from spectrum.nonlinearity import Nonlinearity

import ROOT


class WeighSingleParticleMC(unittest.TestCase):

    def setUp(self):
        self.stop = 'discover' not in sys.argv


    def test_calculate_weights_parameters(self):
        cspectrum = self.corrected_spectrum('nonlin', 5)
        fitf = self.fit_function()
        fitf.SetLineColor(46)

        cyield = cspectrum.evaluate()
        canvas = adjust_canvas(gcanvas(1, 1, True))
        cyield.Fit(fitf)
        cyield.Draw()

        ROOT.gPad.SetLogx()
        ROOT.gPad.SetLogy()
        parameters = map(fitf.GetParameter, range(fitf.GetNpar()))
        print parameters
        wait(save=True)


    @unittest.skip('')
    def test_different_iterations(self):
        w0 = self.corrected_spectrum('nonlin0').evaluate()
        w0.label = 'w0'

        w1 = self.corrected_spectrum('nonlin1').evaluate()
        w1.label = 'w1'

        diff = cmpr.Comparator()
        w1w0 = diff.compare(w1, w0)

        