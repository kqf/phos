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

    def setUp(self):
        self.dataf, self.mcf = 'LHC16', 'Pythia-LHC16-a5'
        self.nonlinearity_file = 'input-data/nonlinearity-{0}.root'.format(self.mcf)


    def getNonlinearityFunction(self):
        func_nonlin = ROOT.TF1("func_nonlin", "[2] * (1.+[0]*TMath::Exp(-x/2*x/2/2./[1]/[1]))", 0, 100);
        func_nonlin.SetParameter(0, -0.05)
        func_nonlin.SetParameter(1, 0.6)
        func_nonlin.SetParameter(2, 1.04)
        return func_nonlin


    def testFitNonlinearityFunction(self):
        ratio = self.getRatio(self.nonlinearity_file)
        function = self.getNonlinearityFunction()
        ratio.SetAxisRange(0.90, 1.08, 'Y')
        ratio.Fit(function)
        ratio.Draw()
        wait(ratio.GetName())


    def getRatio(self, filename):
        try:
            return self.readRatio(filename)
        except IOError:
            return self.calculateRatio(filename)


    def readRatio(self, fname):
        if not os.path.isfile(fname):
            raise IOError('No such file: {0}'.format(fname))

        infile = ROOT.TFile(fname)
        return infile.GetListOfKeys().At(0).ReadObj()


    def calculateRatio(self, fname):
        f = lambda x, y, z: Spectrum(x, label=y, mode = 'd', options = z).evaluate()

        self.data = f(Input('LHC16', 'PhysOnlyTender'), 'Data', Options())
        self.mc = f(Input('Pythia-LHC16-a5', 'PhysRawOnlyTender', 'MassPt'), 'R2D zs 20 MeV nonlin', Options(priority = 1))

        data, mc = self.data[0], self.mc[0]
        data.fifunc = self.getNonlinearityFunction()

        diff = Comparator()
        ratio = diff.compare(data, mc)

        save_tobject(ratio, fname)
        return ratio

