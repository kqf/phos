#!/usr/bin/python

from spectrum.spectrum import Spectrum
from spectrum.input import Input, TimecutInput
from spectrum.sutils import gcanvas
from spectrum.options import Options
from spectrum.sutils import wait
from spectrum.comparator import Visualizer, Comparator
from spectrum.broot import BROOT as br

import ROOT

import os.path
import unittest


class Nonlinearity(unittest.TestCase):

    def setUp(self):
        self.dataf, self.mcf = 'LHC16', 'Pythia-LHC16-a5'
        self.nonlinearity_file = 'input-data/nonlinearity-{0}.root'.format(self.mcf)


    def getNonlinearityFunction(self):
        func_nonlin = ROOT.TF1("func_nonlin", "[2] * (1.+[0]*TMath::Exp(-x/2*x/2/2./[1]/[1]))", 0, 100);
        func_nonlin.SetParNames('A', '#sigma', 'E_{scale}')
        func_nonlin.SetParameter(0, -0.05)
        func_nonlin.SetParameter(1, 0.6)
        func_nonlin.SetParLimits(1, 0, 10)
        func_nonlin.SetParameter(2, 1.04)
        return func_nonlin


    def testFitNonlinearityFunction(self):
        canvas = gcanvas()
        ratio = self.getRatio(self.nonlinearity_file)
        function = self.getNonlinearityFunction()
        ratio.SetAxisRange(0.90, 1.08, 'Y')
        ratio.Fit(function)
        ratio.Draw()

        parameters = map(function.GetParameter, range(function.GetNpar()))
        print 'Nonlinearity parameters: {}'.format(parameters)
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
        f = lambda x, y: Spectrum(x, options = y).evaluate()

        data = f(Input('LHC16', 'PhysOnlyTender'), Options('Data', 'd')).mass
        mc = f(Input('Pythia-LHC16-a5', 'PhysRawOnlyTender'), Options('R2D zs 20 MeV nonlin', 'd')).mass

        data.fitfunc = self.getNonlinearityFunction()
        diff = Comparator()
        ratio = diff.compare(data, mc)

        br.io.save(ratio, fname)
        return ratio

