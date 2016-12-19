#!/usr/bin/python

import ROOT
from array import array

from spectrum.spectrum import PtAnalyzer, Spectrum
from spectrum.sutils import wait
ROOT.TH1.AddDirectory(False)

class Optimizer(object):
    def __init__(self, metrics):
        super(Optimizer, self).__init__()
        self.metrics = metrics

    def minimize(self):
        minuit = ROOT.TMinuit(1)
        minuit.SetFCN(self.metrics.fcn)
        arglist, ierflg = array( 'd', 10*[0.] ),  ROOT.Long(1982)
        # arglist[0] = 1
        minuit.mnexcm( "SET ERR", arglist, 1, ierflg )
        minuit.mnparm( 0, "cut", 50, 1, 20, 100, ierflg)

        # Now ready for minimization step
        arglist[0] = 500
        arglist[1] = 1
        print 'reached here'
        minuit.mnexcm( "MIGRAD", arglist, 2, ierflg )
        p, pe = ROOT.Double(0), ROOT.Double(0)
        minuit.GetParameter(0, p, pe) 
        print 'Estimated value :', p
        self.compare(p)


    def compare(self, pmin):
       res = [PtAnalyzer(*self.metrics.input.extract(pmin)).quantities(), PtAnalyzer(*self.metrics.input.extract(140.e-9)).quantities()]
       import spectrum.comparator as cmpr
       diff = cmpr.Comparator()
       diff.compare_set_of_histograms(res)

if __name__ == '__main__':
   testfit()
