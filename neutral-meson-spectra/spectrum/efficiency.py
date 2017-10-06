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


# TODO: Add efficiecny tests when it will be defined
#

class Efficiency(object):

    def __init__(self, genname, label, iname):
        super(Efficiency, self).__init__()
        self.selection = 'MCStudyOnlyTender'
        self.iname = iname
        self.genname = genname
        self.label = label
        self.oname = 'input-data/efficiency-{0}-{1}.root'.format(self.iname, label)

    def eff(self):
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
        return br.scalew(true)


    def reco(self):
        inp = Input(self.iname, self.selection, 'MassPt')
        reco = Spectrum(inp, Options(self.label, mode = 'q')).evaluate().npi0
        reco.logy = True
        return br.scalew(reco)


    def efficiency(self):
        reco, true = self.reco(), self.true()

        diff = Comparator()
        ratio = diff.compare(reco, true)
        ratio.label = self.label

        if self.oname: 
            br.io.save(ratio, self.oname)
        return ratio
