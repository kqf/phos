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


    def fitfunc(self, bias = 0):
        name = 'tsallis'
        fitf =  ROOT.TF1(name, lambda x, p: sl.tsallis(x, p, bias = bias), 0, 25, 3)
        fitf.SetParameter(0, 2.40)
        fitf.SetParameter(1, 0.139)
        fitf.SetParameter(2, 6.88)
        return fitf

    def fit(self):
        inp, options = Input(self.infile, self.selection), Options('data')
        quantities = Spectrum(inp, options).evaluate()


        spectrum, fitf = quantities.spectrum, self.fitfunc()
        br.scalew(spectrum)
        spectrum.Fit(fitf, '', '')
        spectrum.Draw()
        sl.wait()

        parameters = [fitf.GetParameter(i) for i in range(fitf.GetNpar())]
        lower = self.fitfunc(-0.1)
        upper = self.fitfunc(0.1)
        for i, p in enumerate(parameters):
            lower.SetParameter(i, p)
            upper.SetParameter(i, p)

        lower.Draw()
        upper.Draw('same')
        sl.wait()





    def test(self):
        self.fit()


