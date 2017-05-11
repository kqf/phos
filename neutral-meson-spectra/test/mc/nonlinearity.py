#!/usr/bin/python

from spectrum.spectrum import Spectrum
from spectrum.input import Input, TimecutInput
from spectrum.sutils import get_canvas, adjust_canvas
from spectrum.options import Options
from spectrum.sutils import wait
import ROOT

import unittest


class Nonlinearity(unittest.TestCase):

    def setUp(self):
        f = lambda x, y, z: Spectrum(x, label=y, mode = 'q', options = z).evaluate()
        self.data = f(Input('input-data/LHC16.root', 'PhysTender').read(), 'Data', Options())
        self.mc = f(TimecutInput('input-data/Pythia-LHC16.root', 'TimeTender', 'MassPtN3').read(), 'Run2Default', Options(priority = 1))

    def getNonlinearityFunction(self):
        func_nonlin = ROOT.TF1("func_nonlin", "1.00*(1.+[0]*TMath::Exp(-x/2*x/2/2./[1]/[1]))", 0, 100);
        func_nonlin.SetParameter(0, 1)
        func_nonlin.SetParameter(1, 1)
        return func_nonlin

    def testFitNonlinearityFunction(self):
        c1 = adjust_canvas(get_canvas(1./2, resize = True))
        data, mc = self.data[3], self.mc[3]
        ratio = data.Clone('efficiency_' + data.GetName())

        # Enable binomail errors
        ratio.Divide(data, mc, 1, 1, "B")
        ratio =data 
        label = data.label + ' / ' + mc.label
        ratio.SetTitle('')
        ratio.GetYaxis().SetTitle(label)
        ratio.Draw()

        function = self.getNonlinearityFunction()
        ratio.Fit(function)
        ratio.Draw('same')
        wait(ratio.GetName())
