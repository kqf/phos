#!/usr/bin/python

from spectrum.spectrum import Spectrum
from spectrum.input import Input, TimecutInput
from spectrum.sutils import get_canvas, adjust_canvas
from spectrum.options import Options
from spectrum.sutils import wait
from spectrum.comparator import Visualizer

import ROOT

import unittest


class Nonlinearity(unittest.TestCase):

    def setUp(self):
        f = lambda x, y, z: Spectrum(x, label=y, mode = 'q', options = z).evaluate()
        self.data = f(Input('input-data/LHC16.root', 'PhysTender').read(), 'Data', Options())
        self.mc = f(TimecutInput('input-data/Pythia-LHC16.root', 'TimeTender', 'MassPtN3').read(), 'Run2Default', Options(priority = 1))

    def getNonlinearityFunction(self):
        func_nonlin = ROOT.TF1("func_nonlin", "1.00*(1.+[0]*TMath::Exp(-x/2*x/2/2./[1]/[1]))", 0, 100);
        func_nonlin.SetParameter(0, -0.02)
        func_nonlin.SetParameter(1, 0.7)
        return func_nonlin

    def testFitNonlinearityFunction(self):
        c1 = adjust_canvas(get_canvas(1./2, resize = True))
        data, mc = self.data[2], self.mc[2]

        # TODO: Add possibility to set fit function in comparator.
        # TODO: comparator should return compared ratios? or canvases

        ratio = Visualizer.ratio([data, mc])
        function = self.getNonlinearityFunction()
        ratio.Fit(function)
        ratio.Draw('same')
        wait(ratio.GetName())
