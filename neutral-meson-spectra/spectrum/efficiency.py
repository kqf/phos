#!/usr/bin/python

from spectrum import Spectrum
from options import Options
from .input import Input, read_histogram, SingleHistInput
from comparator import Comparator
from analysis import Analysis
from pipeline import Pipeline, RatioUnion, HistogramSelector

from broot import BROOT as br

import ROOT

import os.path
import unittest


# NB: This test is to compare different efficiencies 
#     estimated from different productions
#

class Efficiency(object):


    def __init__(self, options=Options(), recalculate=False):
        super(Efficiency, self).__init__()
        self.runion = RatioUnion(
            Pipeline([
                Analysis(options.analysis), 
                HistogramSelector("npi0")
            ]),
            SingleHistInput(options.genname)
        )
        self.recalculate = recalculate
        self.oname = 'fixmelater.root'


    def transform(self, inputs, loggs):
        if self.recalculate:
            return self.efficiency(inputs, loggs)
        try:
            return self.read_efficiency(inputs)
        except IOError:
            return self.efficiency(inputs, loggs)


    def read_efficiency(self, inputs):
        if not os.path.isfile(self.oname):
            raise IOError('No such file: {0}'.format(self.oname))

        infile = ROOT.TFile(self.oname)
        result = infile.GetListOfKeys().At(0).ReadObj()
        result.label = inputs.label
        return result

    def efficiency(self, inputs, loggs=None):
        ratio = self.runion.transform(inputs, loggs)
        return ratio




class EfficiencyMultirange(Efficiency):

    def __init__(self, genname, label, inames, recalculate=False, selection='PhysEff', particle="#pi^{0}"):
        super(EfficiencyMultirange, self).__init__(genname, label, '', recalculate, selection)
        self.single_estimators = [
            Efficiency(
                genname, 
                '{0}_{1}_{2}'.format(label, low, upp), 
                filename, 
                recalculate, 
                selection
            ) 
            for filename, (low, upp) in inames.iteritems()
        ]
        self.rranges = inames.values()
        for est, rr in zip(self.single_estimators, self.rranges):
            est.opt = Options.spmc(rr, particle=particle)

        self.recalculate = recalculate

    def efficiency(self):
        effs = [e.eff() for e in self.single_estimators]
        return br.sum_trimm(effs, self.rranges)


    def true(self):
        true = [e.true() for e in self.single_estimators]

        for t in true:
            bin = true[0].FindBin(self.rranges[0][1])
            t.Scale(1. / t.Integral(bin - 1, bin + 1))

        return br.sum_trimm(true, self.rranges)
