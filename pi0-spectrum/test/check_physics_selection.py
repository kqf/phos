import unittest

from spectrum.sutils import get_canvas, wait
from spectrum.spectrum import PtAnalyzer, Spectrum
from spectrum.input import Input, TimecutInput
from test.test_check_different_modules import ModuleAnalyzer
import ROOT
ROOT.TH1.AddDirectory(False)

import numpy as np

def ratio(hist1, hist2, title, label = ''):
    ratio = hist1.Clone(hist1.GetName() + '_ratio')
    ratio.SetTitle(title)
    ratio.label = label

    ratio.Divide(hist2)
    return ratio

def decorate_hist(h, label, logy = False, norm = 1, rebin = 1):
    h.label = label
    h.Rebin(rebin)
    h.Scale(1. / norm)
    if logy: h.logy = logy
    if not h.GetSumw2N(): h.Sumw2()
    return h

def multiple_plot(hists, name):
    canvas = get_canvas(1, 1)
    canvas.Clear()
    canvas.Divide(2, 2)

    for i, h in enumerate(hists):
        canvas.cd(i + 1)
        h.Draw('colz')

    wait(name, True)


class CheckPhysicsSelection(unittest.TestCase):

    def setUp(self):
        self.canvas = get_canvas()

    def test_selection(self):
        hists, multiples = zip(*[self.extract_data('input-data/LHC16l.root', 'old'), self.extract_data('input-data/LHC16l-psel.root', 'PS')])
        multiples = [[h] for h in sum(multiples, [])] 

        import spectrum.comparator as cmpr
        diff = cmpr.Comparator()

        diff.compare_set_of_histograms(hists)
        diff.compare_set_of_histograms(multiples)

    def extract_data(self, filename, label = ''):
        infile = ROOT.TFile(filename)
        phys, time  = infile.PhysTender, infile.TimeTender

        single = self.clusters(phys, label) + self.raw_yield(filename, label) 
        multiple = self.timing(time, label) 

        return single, multiple

    def timing(self, lst, label):
        events = lst.FindObject('EventCounter').GetBinContent(2)
        f = lambda n: decorate_hist(lst.FindObject(n), label, events)

        def hist(h, i):
            axis = h.GetXaxis()
            a, b = axis.FindBin(2), axis.GetNbins() - 1
            time = h.ProjectionY(h.GetName() + "_%s_%d" %(label, i) , a, b) 
            time.SetOption('hist p')
            return decorate_hist(time, label + '> %d GeV' % i, True, 1, 50)

        etimes = [f('hClusterEvsTM%d' % i) for i in range(5)]
        multiple = [hist(etimes[0], i) for i in [1, 4, 8]]
        multiple_plot(etimes[1:], 'e_vs_time_' + label)
        return multiple
  
    def clusters(self, lst, label):
        ## Extract energy of clusters
        events = lst.FindObject('EventCounter').GetBinContent(2)
        f = lambda n: decorate_hist(lst.FindObject(n), label, True, events, 50)
        clusters = [f('hClusterEnergy_SM%d' % i) for i in range(5)]
        main_clusters = [f('hMainClusterEnergy_SM%d' % i) for i in range(5)]

        r = ratio(clusters[0], main_clusters[0], 'Fraction of clusters within 12.5 ns of all clusters', label)
        # Cluster spectrum and fraction of clusters with 12.5ns cut.
        return [clusters[0], decorate_hist(r, label, False)]

    def raw_yield(self, filename, label):
        f = lambda x, y, z: ModuleAnalyzer(x, label=y, mode=z).quantities()
        pi0s = [
                    f(Input(filename, 'PhysTender').read(), label + ' no timecut', 'dead'),
                    f(TimecutInput(filename, 'TimeTender', 'MassPtMainMain').read(), label + ' 12.5 ns', 'dead'), 
               ]

        pi0all, pi0main = pi0s[0][2], pi0s[1][2]
        efficiency = ratio(pi0all, pi0main, 'Timing cut efficiency', label)

        return [efficiency] + pi0s[1]

  