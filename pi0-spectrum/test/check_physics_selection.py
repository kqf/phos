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

def decorate_hist(h, label, logy = False):
    h.Sumw2()
    h.label = label
    if logy: h.logy = logy
    return h


class CheckPhysicsSelection(unittest.TestCase):

    def setUp(self):
        self.canvas = get_canvas()

    def test_selection(self):

        hists = [self.extract_data('input-data/LHC16l-psel.root', 'std'), self.extract_data('input-data/LHC16l-psel.root', 'PS')]

        import spectrum.comparator as cmpr
        diff = cmpr.Comparator()
        diff.compare_set_of_histograms(hists)

    def extract_data(self, filename, label = ''):
        f = lambda x, y, z: PtAnalyzer(x, label=y, mode=z).quantities()
        infile = ROOT.TFile(filename)
        infile.ls()
        phys, time  = infile.PhysTender, infile.TimeTender

        return self.clusters(phys, label) + self.raw_yield(filename, label)

    def clusters(self, lst, label):
        ## Extract energy of clusters
        f = lambda n: decorate_hist(lst.FindObject(n), label, True)
        clusters = [f('hClusterEnergy_SM%d' % i) for i in range(5)]
        main_clusters = [f('hMainClusterEnergy_SM%d' % i) for i in range(5)]
        r = ratio(clusters[0], main_clusters[0], 'Fraction of clusters within 12.5 ns of all clusters', label)
        res = clusters + [decorate_hist(r, label, False)]

        return res 

    def raw_yield(self, filename, label):
        f = lambda x, y, z: PtAnalyzer(x, label=y, mode=z).quantities()
        pi0s = [
                    f(Input(filename, 'PhysTender').read(), label + ' no timecut', 'dead'),
                    f(TimecutInput(filename, 'TimeTender', 'MassPtMainMain').read(), label + ' 12.5 ns', 'dead'), 
               ]

        pi0all, pi0main = pi0s[0][2], pi0s[1][2]
        efficiency = ratio(pi0all, pi0main, 'Timing cut efficiency', label)

        return [efficiency] + pi0s[1]

  