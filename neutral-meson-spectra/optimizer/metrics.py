#!/usr/bin/python

from spectrum.input import TimecutInput
from spectrum.spectrum import PtAnalyzer, Spectrum 
from spectrum.sutils import wait
from math import exp

import ROOT
ROOT.TH1.AddDirectory(False)

class MetricInput(TimecutInput):
    def __init__(self, filename, listname, histname, mixprefix = 'Mix'):
        super(MetricInput, self).__init__(filename, listname, histname, mixprefix)
        self.nevents, self.data, self.mixing = self.read()

    def project(self, cut, draw = False):
        self.data.SetAxisRange(0, cut, 'Z')
        self.mixing.SetAxisRange(0, cut, 'Z')
        data, mixing = self.data.Project3D('yx'), self.mixing.Project3D('yx')

        if draw:
            data.Draw('colz')
            wait('', True)

        return data, mixing
        
    def extract(self, cut):
        data, mixing = self.project(cut)
        return [[self.nevents, data, mixing], 'cut %0.2f' % cut, 'dead']


# Abstract class just to check minimizer interface.
class TestMetrics(object):
    def __init__(self):
        super(TestMetrics, self).__init__()

    def fcn(self, npar, gin, f, par, iflag ):
        f[0] = self.distance(par)

    def distance(self, par):
        x = par[0]
        return (x - 45.1234) ** 2


# Default arguments should be removed
class MaximumSignalMetrics(TestMetrics):
    def __init__(self, inp):
        super(MaximumSignalMetrics, self).__init__()
        self.input = inp 

    def distance(self, par):
        x = par[0] * 1e-9
        singnal = PtAnalyzer(*self.input.extract(x)).quantities()[-1]
        data = [ (singnal.GetBinContent(i) / singnal.GetBinError(i)) ** 2 for i in range(1, singnal.GetNbinsX() + 1) if singnal.GetBinContent(i) > 0 ] 
        return sum(data) ** 2

# Default arguments should be removed
class MaximumDeviationMetrics(MaximumSignalMetrics):
    def __init__(self, inp, reference):
        super(MaximumDeviationMetrics, self).__init__(inp)
        self.reference = self.extract_reference(reference)

    def extract_reference(self, ref):
        return PtAnalyzer(ref.read(), 'no cut', 'dead').quantities()

    def distance(self, par):
        x = par[0] * 1e-9
        spectrum = PtAnalyzer(*self.input.extract(x)).quantities()[2]
        bins = self.ratios(spectrum)
        return -sum(map(lambda x: x ** 2, bins))

    def ratios(self, x):
        ratio = self.reference[2].Clone('ratio_' + self.reference[2].GetName())
        ratio.Divide(x)
        bins = [ratio.GetBinContent(i) / ratio.GetBinError(i) for i in range(1, ratio.GetNbinsX() + 1) if ratio.GetBinContent(i) > 0 ] 
        return bins