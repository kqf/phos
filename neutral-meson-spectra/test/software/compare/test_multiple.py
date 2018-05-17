import unittest

import spectrum.comparator as cmpr
from particles import Particles


class Test(unittest.TestCase, Particles):

    def setUp(self):
        self.data, self.stop = self.config()

    def testCompareRations(self):
        """
            This one is needed to compare "double ratio" plots.
        """
        self.data[0].SetTitle('Test compare: ratios with common baselines')
        diff = cmpr.Comparator(stop=self.stop)
        diff.compare_ratios(self.data, self.data[2])

    def testCompareMultipleRations(self):
        """
            This one is needed to compare "double ratio"
            plots with different baselines.
            The result of this test should give three constant( = 1) graphs.
        """

        self.data[0].SetTitle('Test compare: ratios with different baselines')
        diff = cmpr.Comparator(stop=self.stop)
        diff.compare_multiple_ratios(self.data, self.data)
