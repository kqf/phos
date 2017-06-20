#!/usr/bin/python

from spectrum.input import read_histogram
from spectrum.sutils import wait
from spectrum.comparator import Comparator
from spectrum.ptanalyzer import PtDependent

import ROOT

import os.path
import unittest


class Efficiency(unittest.TestCase):


    def setUp(self):
        self.mc_selection = 'MCStudyOnlyTender'
        self.selection = 'PhysNonlinOnlyTender'
        self.file = 'input-data/Pythia-LHC16-iteration21.root'
        self.labels = ['#bar#Xi^{0}', '#bar#Sigma^{+}', '#bar#Sigma^{*}^{0}', '#bar#Lambda^{0}', '#bar#Delta^{+}', '#bar#Delta^{0}', '#barB^{0}', '#barD^{*}^{0}', '#barD^{0}', 'D^{-}', 'K^{*}^{-}', '#barK^{*}^{0}', '#rho^{-}', 'd', 'u', 's', 'c', 'b', 'g', '#rho^{+}', '#eta', '#omega', 'K_{S^{0}}', 'K^{*}^{0}', 'K^{*}^{+}', "#eta^{'}", '#phi', 'D^{+}', 'D^{0}', 'D^{*}^{0}', 'chi_{^{2}c}', 'dd_{^{1}}', 'ud_{^{0}}', 'ud_{^{1}}', 'neutron', '#Delta^{0}', 'uu_{^{1}}', '#Delta^{+}', '#Lambda^{0}', '#Sigma^{*}^{0}', '#Sigma^{+}', '#Xi^{0}']


    def read(self, x, y, p = 1):
        return read_histogram(self.file, self.mc_selection, x, label = y, priority = p)


    def testDifferentContributions(self):
        filename = 'hPtGeneratedMC_#pi^{0}'
        labels = 'secondary', '#pi^{-}', '#pi^{+}', '#eta', '#omega', 'K_0^s', '#Lambda'

        hists = map(lambda x: self.read('{0}_{1}'.format(filename, x),  x, 999), labels)
        hists[0].logy = True

        map(PtDependent.divide_bin_width, hists)

        diff = Comparator()
        diff.compare(hists)

        pall = self.read(filename, 'all', -1)
        pall.logy = True

        pprimary = self.read(filename + '_primary', 'primary', 999)
        pprimary.logy = True

        map(PtDependent.divide_bin_width, (pall, pprimary))
        diff.compare(pprimary, pall)


    def adjustBins(self, hist):
        assert hist.GetNbinsX() == len(self.labels), 'self.Labels and histogram have different length'
        nhist = ROOT.TH1F('{}_binned'.format(hist.GetName()), hist.GetTitle(), len(self.labels), 0, len(self.labels))

        for i, l in enumerate(self.labels):
            nhist.SetBinContent(i + 1, hist.GetBinContent(i + 1))
            nhist.SetBinError(i + 1, hist.GetBinError(i + 1))
            nhist.GetXaxis().SetBinLabel(i + 1, l)

        if 'label' in dir(hist):
            nhist.label = hist.label

        if 'priority' in dir(hist):
            nhist.priority = hist.priority

        nhist.SetOption('l')

  
        return nhist


    def testSources(self):
        filename = 'hMC_#pi^{0}_sources'
        labels = 'primary', 'secondary'
        hists = map(lambda x: self.read('{0}_{1}'.format(filename, x),  x, 999), labels)
        hists = map(self.adjustBins, hists)
        map(lambda x: x.Scale(1./x.Integral()), hists)

        hists[0].logy = True
        diff = Comparator()
        diff.compare(hists[::-1])





   



