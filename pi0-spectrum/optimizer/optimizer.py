#!/usr/bin/python

import ROOT
from array import array

from spectrum.spectrum import PtAnalyzer, Spectrum
from spectrum.sutils import wait
ROOT.TH1.AddDirectory(False)

class Input(object):
    def __init__(self, filename, histname, f = lambda x: x.TimeTender):
        super(Input, self).__init__()
        self.nevents, self.data, self.mixing = self.read(filename, histname, f)

    def read(self, filename, histname, f):
        nevents = ROOT.TFile(filename).PhysTender.FindObject('EventCounter').GetBinContent(2)
        lst = f(ROOT.TFile(filename))
        rawhist, rawmix = lst.FindObject('h' + histname), lst.FindObject('hMix' + histname)
        return nevents, rawhist, rawmix

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


class Optimizer(object):
    def __init__(self, filename, histname):
        super(Optimizer, self).__init__()
        self.inp = Input(filename, histname)
        self.minimize()

    def minimize(self):
        minuit = ROOT.TMinuit(1)
        minuit.SetFCN(self.fcn)
        arglist, ierflg = array( 'd', 10*[0.] ),  ROOT.Long(1982)
        # arglist[0] = 1
        minuit.mnexcm( "SET ERR", arglist, 1, ierflg )
        minuit.mnparm( 0, "cut", 50, 1, 20, 100, ierflg)

        # Now ready for minimization step
        arglist[0] = 500
        arglist[1] = 1
        minuit.mnexcm( "MIGRAD", arglist, 2, ierflg )
        p, pe = ROOT.Double(0), ROOT.Double(0)
        minuit.GetParameter(0, p, pe) 
        self.compare(p)

    def fcn(self, npar, gin, f, par, iflag ):
        x = par[0] * 1e-9
        singnal = PtAnalyzer(*self.inp.extract(x)).quantities()[-1] 

        data = [singnal.GetBinContent(i) / singnal.GetBinError(i) for i in range(1, singnal.GetNbinsX() + 1) if singnal.GetBinContent(i) > 0 ] 
        bins = sum(data)
        print bins
        f[0] = bins

    def compare(self, pmin):
       res = [PtAnalyzer(*self.inp.extract(pmin)).quantities(), PtAnalyzer(*self.inp.extract(140.e-9)).quantities()]
       import spectrum.comparator as cmpr
       diff = cmpr.Comparator()
       # diff.compare_lists_of_histograms([first, second])
       diff.compare_set_of_histograms(res)

if __name__ == '__main__':
   testfit()
