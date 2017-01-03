import unittest

from spectrum.sutils import get_canvas, wait
from spectrum.spectrum import PtAnalyzer, Spectrum
from spectrum.input import Input, TimecutInput
import ROOT
ROOT.TH1.AddDirectory(False)

import numpy as np

def ratio(hist1, hist2, title, label = ''):
    ratio = hist1.Clone(hist1.GetName() + '_ratio')
    ratio.SetTitle(title)
    ratio.label = label

    ratio.Divide(hist2)
    return ratio

def decorate_hist(h, label, logy = False, norm = 1):
    h.Sumw2()
    h.label = label
    # h.Rebin(20)
    h.Scale(1. / norm)
    if logy: h.logy = logy
    return h

class CheckPhysicsSelection(unittest.TestCase):

    def setUp(self):
        self.canvas = get_canvas()

    def test_selection(self):
        hists, multiples = zip(*[self.extract_data('input-data/LHC16l.root', 'old'), self.extract_data('input-data/LHC16l-psel.root', 'PS')])

        import spectrum.comparator as cmpr
        diff = cmpr.Comparator()
        # diff.compare_set_of_histograms(hists)
        diff.compare_multiple(multiples)

    def extract_data(self, filename, label = ''):
        f = lambda x, y, z: PtAnalyzer(x, label=y, mode=z).quantities()
        infile = ROOT.TFile(filename)
        infile.ls()
        phys, time  = infile.PhysTender, infile.TimeTender

        single, multiple = self.clusters(phys, label) 

        single = single + self.raw_yield(filename, label) 
        multiple = self.timing(time, label) + multiple
        return single, multiple

    def timing(self, lst, label):
        events = lst.FindObject('EventCounter').GetBinContent(2)
        f = lambda n: decorate_hist(lst.FindObject(n), label, events)

        def hist(h, i):
            axis = h.GetXaxis()
            a, b = axis.FindBin(2), axis.GetNbins() - 1
            time = h.ProjectionY(h.GetName() + "_%s_%d" %(label, i) , a, b) 
            return decorate_hist(time, label + '> %d GeV' % i, True)

        events = [f('hClusterEvsTM%d' % i) for i in range(5)]
        multiple = [[hist(h, i) for h in events[1:]] for i in [1, 4, 5]]
        return multiple
  
    def clusters(self, lst, label):
        ## Extract energy of clusters
        events = lst.FindObject('EventCounter').GetBinContent(2)
        f = lambda n: decorate_hist(lst.FindObject(n), label, True, events)
        clusters = [f('hClusterEnergy_SM%d' % i) for i in range(5)]
        main_clusters = [f('hMainClusterEnergy_SM%d' % i) for i in range(5)]

        r = ratio(clusters[0], main_clusters[0], 'Fraction of clusters within 12.5 ns of all clusters', label)
        return [decorate_hist(r, label, False)], [clusters[1:]]

    def raw_yield(self, filename, label):
        f = lambda x, y, z: PtAnalyzer(x, label=y, mode=z).quantities()
        pi0s = [
                    f(Input(filename, 'PhysTender').read(), label + ' no timecut', 'dead'),
                    f(TimecutInput(filename, 'TimeTender', 'MassPtMainMain').read(), label + ' 12.5 ns', 'dead'), 
               ]

        pi0all, pi0main = pi0s[0][2], pi0s[1][2]
        efficiency = ratio(pi0all, pi0main, 'Timing cut efficiency', label)

        return [efficiency] + pi0s[1]

  