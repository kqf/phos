#!/usr/bin/python


from spectrum.input import TimecutInput
from spectrum.spectrum import PtAnalyzer, Spectrum
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


# Default arguments should be removed
class Metrics(object):
    def __init__(self, inp = None, reference = None):
        super(Metrics, self).__init__()
        self.reference = reference
        self.input = inp

    def fcn(self, npar, gin, f, par, iflag ):
        f[0] = self.distance(par)

    def distance(self, par):
        x = par[0]
        return (x - 45.1234) ** 2
        # singnal = PtAnalyzer(*self.inp.extract(x)).quantities()[-1]
        # data = [singnal.GetBinContent(i) / singnal.GetBinError(i) for i in range(1, singnal.GetNbinsX() + 1) if singnal.GetBinContent(i) > 0 ] 
        # bins = sum(data)
