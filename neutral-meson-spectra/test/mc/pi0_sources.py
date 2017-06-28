#!/usr/bin/python

from spectrum.input import read_histogram
from spectrum.sutils import wait
from spectrum.comparator import Comparator
from spectrum.ptanalyzer import PtDependent

import ROOT

import os.path
import unittest


class Pi0Sources(unittest.TestCase):


    def setUp(self):
        self.mc_selection = 'MCStudyOnlyTender'
        self.selection = 'PhysNonlinOnlyTender'
        self.file = 'input-data/Pythia-LHC16-a1.root'
        self.filename = 'hPtGeneratedMC_#pi^{0}'
        self.labels = {'#pi^{-}': -211, 'K_{S}^{0}': 310, '#omega': 223, '#rho^{-}': -213, '#pi^{+}': 211, '#Lambda^{0}': 3122, '#rho^{+}': 213, '#eta': 221}
        self.labels = {self.labels[i]: i for i in self.labels}


    def read(self, x, y, p = 1):
        return read_histogram(self.file, self.mc_selection, x, label = y, priority = p)


    def testDifferentContributions(self):
        def contribution(contr_type = 'secondary'):
            filename = self.filename + '_' + contr_type 
            labels = '', '#pi^{-}', '#pi^{+}', '#eta', '#omega', 'K^{s}_{0}', '#Lambda', '#rho^{-}', '#rho^{+}'

            print map(lambda x: '{0}_{1}'.format(filename, x), labels)
            hists = map(lambda x: self.read('{0}_{1}'.format(filename, x),  x, 999), labels)
            hists[0].logy = True

            map(PtDependent.divide_bin_width, hists)

            diff = Comparator()
            diff.compare(hists)

            pall = self.read(self.filename, 'all', -1)
            pall.logy = True

            pprimary = self.read(self.filename + '_primary_', 'primary', 999)
            pprimary.logy = True

            map(PtDependent.divide_bin_width, (pall, pprimary))
            # diff.compare(pprimary, pall)
            diff = Comparator(crange = (1e-9, 1))
            diff.compare_ratios(hists, pall, logy = True)

        contribution('secondary')
        contribution('primary')


    def adjustBins(self, hist):
        nhist = ROOT.TH1F('{}_binned'.format(hist.GetName()), hist.GetTitle(), len(self.labels), 0, len(self.labels))

        bins = {i: int(hist.GetBinCenter(i) - 0.5) for i in range(1, hist.GetNbinsX() + 1) if hist.GetBinContent(i) > 0}
        nbins = hist.GetNbinsX()

        assert len(bins) == len(self.labels), "You have different number of labels and particles"
        for i, bin in enumerate(bins):
            nhist.SetBinContent(i + 1, hist.GetBinContent(bin))
            nhist.SetBinError(i + 1, hist.GetBinError(bin))
            nhist.GetXaxis().SetBinLabel(i + 1, self.labels[bins[bin]])

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
        hists[0].SetLabelSize(hists[0].GetLabelSize('X') * 2., 'X')
        hists[0].SetTitleOffset(hists[0].GetTitleOffset('X') * 6. , 'X')
        diff = Comparator()
        diff.compare(hists)





   



