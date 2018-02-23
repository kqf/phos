#!/usr/bin/python

from spectrum import Spectrum
from options import Options
from .input import Input, read_histogram
from comparator import Comparator

from broot import BROOT as br

import ROOT

import os.path
import unittest


# NB: This test is to compare different efficiencies 
#     estimated from different productions
#

class Efficiency(object):

    def __init__(self, genname, label, iname, recalculate = False, 
            selection = 'MCStudyOnlyTender', opt = Options(mode = 'd')):
        super(Efficiency, self).__init__()
        self.recalculate = recalculate
        self.selection = selection
        self.genname = genname
        self.label = label
        self.iname = iname
        self.oname = 'input-data/efficiency-{0}-{1}.root'.format(self.iname, label)
        self.opt = opt
        self.opt.label = label


    def eff(self):
        if self.recalculate:
            return self.efficiency()

        try:
            return self.read_efficiency()
        except IOError:
            return self.efficiency()


    def read_efficiency(self):
        if not os.path.isfile(self.oname):
            raise IOError('No such file: {0}'.format(self.oname))

        infile = ROOT.TFile(self.oname)
        result = infile.GetListOfKeys().At(0).ReadObj()
        result.label = self.label
        return result


    def true(self, label = 'Generated'):
        true = read_histogram(self.iname, self.selection, self.genname, label = label, priority = 0)
        true.logy = True
        return true 


    def reco(self):
        inp = Input(self.iname, self.selection, 'MassPt', label=self.label)
        reco = Spectrum(inp, self.opt).evaluate().npi0
        reco.logy = True
        return reco

    def efficiency(self):
        reco, true = self.reco(), self.true()
        diff = Comparator()

        true.label = "generated primary"
        reco.label = "reconstructed"
        # This is the correct pattern
        true, reco = br.rebin_as(true, reco)
        br.scalew(reco)
        br.scalew(true)

        ratio = diff.compare(reco, true)
        ratio.label = self.label

        if self.oname: 
            br.io.save(ratio, self.oname)
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
