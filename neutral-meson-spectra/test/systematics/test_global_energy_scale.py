from spectrum.spectrum import Spectrum
from spectrum.input import Input
from spectrum.options import Options
from spectrum.comparator import Comparator

from spectrum.broot import BROOT as br
import spectrum.sutils as sl

import ROOT

import os.path
import unittest


class TestGlobalEnergyScaleUncetanity(unittest.TestCase):

    def setUp(self):
        # This should be studied on corrected yield
        #
        self.infile = 'LHC16'
        self.selection = 'PhysOnlyTender'


    def fitfunc(self):
        name = 'tsallis'
        fitf =  ROOT.TF1(name, sl.tsallis, 0, 25, 3)
        # TODO: Figure out the start parameters for the fit
        return fitf

    def fit(self):
        inp, options = Input(self.infile, self.selection), Options('data')
        # quantities = Spectrum(inp, options).evaluate()
        quantities = inp
        quantities.spectrum = ROOT.TH1F('h', 'gaus', 100, 0, 20)
        quantities.spectrum.FillRandom('gaus')


        spectrum, fitf = quantities.spectrum, self.fitfunc()
        br.scalew(spectrum)
        spectrum.Fit(fitf, '', '')
        spectrum.Draw()
        sl.wait()


    def test(self):
        self.fit()


