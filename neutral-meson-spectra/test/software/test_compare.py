
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

    def testCompareMultiple(self):
        diff = cmpr.Comparator()
        diff.compare_set_of_histograms(zip(*[self.data, self.data]))

    @unittest.skip('test')
    def testCompareTwo(self):
        diff = cmpr.Comparator()
        diff.compare_set_of_histograms([[self.data[2]], [self.data[1]]])

    @unittest.skip('test')
    def testCompareTwoWithFit(self):
        diff = cmpr.Comparator(ratiofit=(0, 0))
        diff.compare_set_of_histograms([[self.data[2]], [self.data[1]]])

        diff = cmpr.Comparator(ratiofit=(0, 10))
        diff.compare_set_of_histograms([[self.data[2]], [self.data[1]]])

        diff = cmpr.Comparator(ratiofit=(5, 10))
        diff.compare_set_of_histograms([[self.data[2]], [self.data[1]]])

        diff = cmpr.Comparator(ratiofit=(5, 0))
        diff.compare_set_of_histograms([[self.data[2]], [self.data[1]]])

    @unittest.skip('test')
    def testCompareSingle(self):
        diff = cmpr.Comparator()
        diff.compare_set_of_histograms( [[self.data[1], self.data[2]]] )

    @unittest.skip('test')
    def testCompareRations(self):
        diff = cmpr.Comparator()
        diff.compare_ratios(self.data, self.data[2])

    @unittest.skip('test')
    def testSuccesive(self):
        """
            Explanation:
                This is needed to check if behaviour changes after double usage of a comparator.
                Also this test assures that comparison "A" and "B" and "B" and "A" work as needed.
        """

        diff = cmpr.Comparator()
        diff.compare_set_of_histograms([[self.data[2]], [self.data[1]]])

        diff.compare_set_of_histograms([[self.data[2]], [self.data[1]]])

        diff.compare_set_of_histograms([[self.data[1]], [self.data[2]]])







