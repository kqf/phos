#!/usr/bin/python

from spectrum.input import TimecutInput
from spectrum.spectrum import KinematicTransformer, Spectrum 
from spectrum.sutils import wait
from math import exp

import ROOT
ROOT.TH1.AddDirectory(False)

class MetricInput(TimecutInput):
    def __init__(self, filename, listname, histname, mixprefix = 'Mix'):
        super(MetricInput, self).__init__(filename, listname, histname, mixprefix)
        self.data_mixing = self.read()

    def _project(self, cut, rhist, draw = False):
        rhist.SetAxisRange(0, cut, 'Z')
        hist = rhist.Project3D('yx')

        if draw:
            hist.Draw('colz')
            wait('', True)
        return hist

    def project(self, cut, draw):
        return map(
            lambda x: self._project(cut, x, draw),
            self.data_mixing
            )
        
    def extract(self, cut):
        data_mixing = map(lambda x: self._project(cut, x), self.data_mixing)
        return [data_mixing, 'cut %0.2f' % cut, 'dead']


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
        singnal = KinematicTransformer(*self.input.extract(x)).quantities()[-1]
        data = [ (singnal.GetBinContent(i) / singnal.GetBinError(i)) ** 2 for i in range(1, singnal.GetNbinsX() + 1) if singnal.GetBinContent(i) > 0 ] 
        return sum(data) ** 2

# Default arguments should be removed
class MaximumDeviationMetrics(MaximumSignalMetrics):
    def __init__(self, inp, reference):
        super(MaximumDeviationMetrics, self).__init__(inp)
        self.reference = self.extract_reference(reference)

    def extract_reference(self, ref):
        return KinematicTransformer(ref.read(), 'no cut', 'dead').quantities()

    def distance(self, par):
        x = par[0] * 1e-9
        spectrum = KinematicTransformer(*self.input.extract(x)).quantities()[2]
        bins = self.ratios(spectrum)
        return -sum(map(lambda x: x ** 2, bins))

    def ratios(self, x):
        ratio = self.reference[2].Clone('ratio_' + self.reference[2].GetName())
        ratio.Divide(x)
        bins = [ratio.GetBinContent(i) / ratio.GetBinError(i) for i in range(1, ratio.GetNbinsX() + 1) if ratio.GetBinContent(i) > 0 ] 
        return bins