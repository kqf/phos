#!/usr/bin/python

from spectrum.input import read_histogram
from spectrum.sutils import wait
from spectrum.comparator import Comparator
from spectrum.ptanalyzer import PtDependent, scalew

import ROOT

import os.path
import unittest


class Pi0Sources(unittest.TestCase):


    def setUp(self):
        self.mc_selection = 'MCStudyOnlyTender'
        self.selection = 'PhysNonlinOnlyTender'
        # self.file = 'input-data/scaled-LHC17f8a.root'
        self.file = 'input-data/Pythia-LHC16-a4.root'
        self.histname = 'hPt_#pi^{0}'
        # self.labels = {'#pi^{-}': -211, 'K_{S}^{0}': 310, '#omega': 223, '#rho^{-}': -213, '#pi^{+}': 211, '#Lambda^{0}': 3122, '#rho^{+}': 213, '#eta': 221}

        self.sorted_labels = ['K^{*0}', '#barK^{*0}', 'K^{*-}', 'K^{*+}', 'c', 'K_{S}^{0}', 'g', 's', '#eta', '#omega', 'd', 'u', '#rho^{-}', '#rho^{+}']
        self.labels = {'c': 4, 'd': 1, 'g': 21, 'K_{S}^{0}': 310, '#omega': 223, '#rho^{-}': -213, '#barK^{*0}': -313, '#rho^{+}': 213, 's': 3, 'u': 2, '#eta': 221, 'K^{*-}': -323, 'K^{*0}': 313, 'K^{*+}': 323}
        self.cut = 1e-2


    def read(self, x, y, p = 1):
        return read_histogram(self.file, self.mc_selection, x, label = y, priority = p)


    @unittest.skip('')
    def testDifferentContributions(self):
        def contribution(contr_type = 'secondary'):
            filename = self.histname + '_' + contr_type 
            labels = '', '#pi^{-}', '#pi^{+}', '#eta', '#omega', 'K^{s}_{0}', '#Lambda', '#rho^{-}', '#rho^{+}'

            print map(lambda x: '{0}_{1}'.format(filename, x), labels)
            hists = map(lambda x: self.read('{0}_{1}'.format(filename, x),  x, 999), labels)
            hists[0].logy = True

            map(scalew, hists)

            diff = Comparator()
            diff.compare(hists)

            pall = self.read(self.histname, 'all', -1)
            pall.logy = True

            pprimary = self.read(self.histname + '_primary_', 'primary', 999)
            pprimary.logy = True

            map(scalew, (pall, pprimary))
            # diff.compare(pprimary, pall)
            diff = Comparator(crange = (1e-9, 1))
            diff.compare_ratios(hists, pall, logy = True)

        contribution('secondary')
        contribution('primary')


    def mostProbableBins(self, hist):
        nhist = hist.Clone(hist.GetName() + 'checking_the_main_contributors')
        nhist.label = hist.label
        nhist.Scale(1./ nhist.Integral())
        bins = {int(nhist.GetBinCenter(i) - 0.5): nhist.GetBinContent(i) for i in range(1, nhist.GetNbinsX() + 1) if nhist.GetBinContent(i) > self.cut }

        total = 0
        for k in sorted(bins.keys()):
            print '{0}: {1}'.format(k, bins[k])
            total += bins[k]

        print bins.keys()

        print 'The selecte bins sum up to {0} percent of the histogram.'.format(total)
        return nhist


    def adjustBins(self, hist):
        nhist = ROOT.TH1F('{}_binned'.format(hist.GetName()), hist.GetTitle(), len(self.labels), 0, len(self.labels))

        hist = self.mostProbableBins(hist)

        for l in self.labels:
            print self.labels[l]

        # data = {hist.GetBinContent(hist.FindBin(self.labels[l])): l for l in self.labels}
        # print [data[l] for l in sorted(data.keys())]

        for i, l in enumerate(self.sorted_labels):
            bin = hist.FindBin(self.labels[l])
            nhist.SetBinContent(i + 1, hist.GetBinContent(bin))
            nhist.SetBinError(i + 1, hist.GetBinError(bin))
            nhist.GetXaxis().SetBinLabel(i + 1, l)

        if 'label' in dir(hist):
            nhist.label = hist.label

        if 'priority' in dir(hist):
            nhist.priority = hist.priority

        nhist.SetOption('l')
        return nhist


    def testSources(self):
        filename = 'hMC_#pi^{0}_sources'
        labels =  'secondary', 'primary'
        hists = map(lambda x: self.read('{0}_{1}'.format(filename, x),  x, 999), labels)
        hists = map(self.adjustBins, hists)
        map(lambda x: x.Scale(1./x.Integral()), hists)

        hists[0].logy = True
        hists[0].SetLabelSize(hists[0].GetLabelSize('X') * 2., 'X')
        hists[0].SetTitleOffset(hists[0].GetTitleOffset('X') * 6. , 'X')
        diff = Comparator()
        diff.compare(hists)

