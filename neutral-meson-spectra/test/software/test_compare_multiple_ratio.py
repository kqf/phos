
import unittest
import ROOT
import json


import spectrum.comparator as cmpr
from test.software.test_compare import get_spectrum


class Test(unittest.TestCase):

    def setUp(self):
        with open('config/test_particles.json') as f: 
            particles = json.load(f)
        self.data = [get_spectrum(i, *particles[i]) for i in particles]


    def testCompareRations(self):
        """
            This one is needed to compare "double ratio" plots.
        """
        diff = cmpr.Comparator()
        diff.compare_ratios(self.data, self.data[2])

    def testCompareMultipleRations(self):
        """
            This one is needed to compare "double ratio" plots with different baselines.
            The result of this test should give three constant( = 1) graphs.
        """

        diff = cmpr.Comparator()
        diff.compare_multiple_ratios(self.data, self.data) 
