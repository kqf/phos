#!/usr/bin/python

from spectrum.spectrum import Spectrum
from spectrum.input import Input, TimecutInput
from spectrum.sutils import get_canvas, adjust_canvas
from spectrum.options import Options
from spectrum.sutils import wait
from spectrum.comparator import Visualizer

import ROOT

import os.path
import unittest


class Nonlinearity(unittest.TestCase):


    def getNonlinearityFunction(self):
        func_nonlin = ROOT.TF1("func_nonlin", "[2] * (1.+[0]*TMath::Exp(-x/2*x/2/2./[1]/[1]))", 0, 100);
        func_nonlin.SetParameter(0, -1.03621e+00)
        func_nonlin.SetParameter(1, 7.76573e-01)
        func_nonlin.SetParameter(2, 4)
        return func_nonlin

    def testFitNonlinearityFunction(self):
        c1 = adjust_canvas(get_canvas(1., resize = True))
        fname = 'datamcratio.root'
        ratio = self.readRatio(fname) if os.path.isfile(fname) else self.getRatio(fname)
        function = self.getNonlinearityFunction()
        ratio.SetAxisRange(0, 10, 'Y')
        ratio.Fit(function)
        ratio.Draw()
        wait(ratio.GetName())

    def readRatio(self, fname):
        infile = ROOT.TFile(fname)
        return infile.GetListOfKeys().At(0).ReadObj()

    def getRatio(self, fname):
        f = lambda x, y, z: Spectrum(x, label=y, mode = 'q', options = z).evaluate()
        self.data = f(Input('input-data/LHC16.root', 'PhysTender').read(), 'Data', Options())
        self.mc = f(TimecutInput('input-data/Pythia-LHC16.root', 'TimeTender', 'MassPtN3').read(), 'Run2Default', Options(priority = 1))
        c1 = adjust_canvas(get_canvas(1./2, resize = True))
        data, mc = self.data[2], self.mc[2]

        # TODO: Add possibility to set fit function in comparator.
        # TODO: comparator should return compared ratios? or canvases

        ratio = Visualizer.ratio([data, mc])

        ofile = ROOT.TFile(fname, 'recreate')
        ratio.Write()
        ofile.Close()
        return ratio


