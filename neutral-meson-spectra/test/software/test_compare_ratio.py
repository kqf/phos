
import unittest
import ROOT
import json


from math import sqrt
from spectrum.sutils import tsallis
import spectrum.comparator as cmpr
from test.software.test_compare import get_spectrum


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

    # @unittest.skip('test')
    def testCompareTwoWithFit(self):
        """
            Checks multiple fitting ranges. 
        """
   
        diff = cmpr.Comparator(ratiofit=(0, 0))
        diff.compare_set_of_histograms([[self.data[2]], [self.data[1]]])

        diff = cmpr.Comparator(ratiofit=(0, 10))
        diff.compare_set_of_histograms([[self.data[2]], [self.data[1]]])

        diff = cmpr.Comparator(ratiofit=(5, 10))
        diff.compare_set_of_histograms([[self.data[2]], [self.data[1]]])

        diff = cmpr.Comparator(ratiofit=(5, 0))
        diff.compare_set_of_histograms([[self.data[2]], [self.data[1]]])

    # @unittest.skip('test')
    def testCompareRations(self):
        """
            This one is needed to compare "double ratio" plots.
        """
        diff = cmpr.Comparator()
        diff.compare_ratios(self.data, self.data[2])

   # @unittest.skip('test')
    def testCompareRations(self):
        diff = cmpr.Comparator()
        diff.compare_ratios(self.data, self.data[2]) 