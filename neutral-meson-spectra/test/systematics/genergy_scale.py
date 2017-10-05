from spectrum.input import Input
from spectrum.options import Options
from spectrum.spectrum import Spectrum
from spectrum.comparator import Comparator

from spectrum.broot import BROOT as br
import spectrum.sutils as sl

from systematic_error import SysError

import ROOT

import os.path
import unittest


# CWR: Run this on corrected spectrum 
# 

class GlobalEnergyScaleUncetanityEvaluator(object):

    def __init__(self, stop):
        super(GlobalEnergyScaleUncetanityEvaluator, self).__init__()
        # This should be studied on corrected yield
        #
        self.infile = 'LHC16'
        self.selection = 'PhysOnlyTender'
        self.stop = True or stop 
        self.outsys = SysError(label = 'global energy scale')


    @staticmethod
    def ratiofunc(fitf, name = '' ,bias = 0.01, color = 46):
        rf = lambda x, p: sl.tsallis([x[0] + x[0] * bias] , p) / sl.tsallis(x, p)
        rfunc = ROOT.TF1(name, rf, 0, 25, 3)
        pars, _ = br.pars(fitf)
        rfunc.SetParameters(*pars)
        rfunc.SetLineColor(color)
        return rfunc


    @classmethod
    def fitfunc(klass, name = '' ,bias = 0):
        fitf =  ROOT.TF1(name, lambda x, p: sl.tsallis(x, p, bias = bias), 0, 25, 3)
        fitf.SetParameter(0, 2.40)
        fitf.SetParameter(1, 0.139)
        fitf.SetParameter(2, 6.88)
        return fitf

    def fit(self):
        inp, options = Input(self.infile, self.selection), Options('data')
        quantities = Spectrum(inp, options).evaluate()
        spectrum, fitf = quantities.spectrum, self.fitfunc('tsallis_')
        br.scalew(spectrum)
        spectrum.Fit(fitf, '', '')
        spectrum.Draw()

        diff = Comparator(stop = self.stop)
        diff.compare(spectrum)

        lower = self.ratiofunc(fitf,'low', -0.01, 38)
        upper = self.ratiofunc(fitf,'up', 0.01, 47)

        diff = Comparator(stop = self.stop, rrange = (-1, ))
        diff.compare(lower, upper)
        return spectrum, lower, upper


    def test_systematics(self):
        spectrum, lower, upper = self.fit()
        syst_error = self.outsys.histogram(spectrum)
        bins = [syst_error.GetBinCenter(i) for i in br.range(syst_error)]
        bins = [upper.Eval(c) - lower.Eval(c) for c in bins]
        for i, b in enumerate(bins):
            if b < 0:
                print 'Warning: negative global energy scale corrections'
            syst_error.SetBinContent(i + 1, abs(b))
        return syst_error
