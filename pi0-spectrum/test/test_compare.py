
import unittest
import ROOT
import json


from math import sqrt
import spectrum.comparator as cmpr

def tsallis(x, p, a, b):
    return x[0]*p[0]/2./3.1415*(p[2]-1.)*(p[2]-2.)/(p[2]*p[1]*(p[2]*p[1]+b*(p[2]-2.))) * (1.+(sqrt(x[0]*x[0]+a*a)-b)/(p[2]*p[1])) ** (-p[2])

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
        with open('test/particles.json') as f: 
            particles = json.load(f)
        self.data = [get_spectrum(i, *particles[i]) for i in particles]

    def testCompareMultiple(self):
        diff = cmpr.Comparator()
        diff.compare_set_of_histograms(zip(*[self.data, self.data]))

    def testCompareTwo(self):
        diff = cmpr.Comparator()
        diff.compare_set_of_histograms([[self.data[2]], [self.data[1]]])
