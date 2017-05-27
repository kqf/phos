#!/usr/bin/python

from spectrum.spectrum import Spectrum
from spectrum.input import Input, TimecutInput
from spectrum.sutils import get_canvas, adjust_canvas
from spectrum.options import Options
from spectrum.sutils import wait
from spectrum.comparator import Visualizer, Comparator
from spectrum.sutils import save_tobject

import ROOT

import os.path
import unittest


class Nonlinearity(unittest.TestCase):


    def getNonlinearityFunction(self):
        func_nonlin = ROOT.TF1("func_nonlin", "[2] * (1.+[0]*TMath::Exp(-x/2*x/2/2./[1]/[1]))", 0, 100);
        func_nonlin.SetParameter(0, -0.05)
        func_nonlin.SetParameter(1, 0.6)
        func_nonlin.SetParameter(2, 1.04)
        return func_nonlin


    def testFitNonlinearityFunction(self):
        c1 = adjust_canvas(get_canvas(1., resize = True))
        fname = 'datamcratio.root'
        ratio = self.readRatio(fname) if os.path.isfile(fname) else self.getRatio(fname)
        function = self.getNonlinearityFunction()
        ratio.SetAxisRange(0.90, 1.08, 'Y')
        ratio.Fit(function)
        ratio.Draw()
        wait(ratio.GetName())


    def readRatio(self, fname):
        infile = ROOT.TFile(fname)
        return infile.GetListOfKeys().At(0).ReadObj()


    def getRatio(self, fname):
        f = lambda x, y, z: Spectrum(x, label=y, mode = 'q', options = z).evaluate()

        self.data = f(Input('input-data/LHC16.root', 'PhysTender').read(), 'Data', Options())
        self.mc = f(TimecutInput('input-data/Pythia-LHC16-iteration13.root', 'PhysTender', 'MassPtN3').read(), 'R2D zs 20 MeV', Options(priority = 1))
        # self.mc = f(TimecutInput('input-data/Pythia-LHC16-iteration7.root', 'PhysTender', 'MassPtN3').read(), 'LHC16all 20MeV', Options(priority = 1))

        data, mc = self.data[0], self.mc[0]
        data.fifunc = self.getNonlinearityFunction()

        diff = Comparator()
        ratio = diff.compare_set_of_histograms([[data], [mc]])[0]

        save_tobject(ratio, fname)
        return ratio

