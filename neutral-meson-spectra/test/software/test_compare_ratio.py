
import unittest
import ROOT
import json


from math import sqrt
from spectrum.sutils import tsallis
import spectrum.comparator as cmpr



def get_spectrum(name, a, b, par):
    function = ROOT.TF1('f' + name, lambda x, p: tsallis(x, p, a, a), 0.3, 15, 3)
    function.SetParameters(*par)
    histogram = ROOT.TH1F(name + '_spectrum', '%s p_{T} spectrum; p_{T}, GeV/c' % name, 100, 0.3, 15)
    histogram.FillRandom('f' + name, 1000000)
    histogram.label = name
    histogram.Sumw2()
    return histogram

class Test(unittest.TestCase):

    def setUp(self):
        with open('config/test_particles.json') as f: 
            particles = json.load(f)
        self.data = [get_spectrum(i, *particles[i]) for i in particles]


    def testCompareRatio(self):
        diff = cmpr.Comparator()
        main = self.data[1]
        distorted = main.Clone(main.GetName() + '_clone')
        distorted.SetBinContent(80, distorted.GetBinContent(80) * 100)
        distorted.label = 'distorted'
        diff.compare_set_of_histograms([[main], [distorted]])
