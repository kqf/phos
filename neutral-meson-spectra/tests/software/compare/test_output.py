import unittest

import spectrum.comparator as cmpr
from spectrum.sutils import wait, gcanvas
from particles import Particles


class TestOutputRatio(unittest.TestCase, Particles):
    """
         This test is needed to check if comparator
         returns ratio histogram correctly
         or none object when it's not relevant.
    """

    def setUp(self):
        self.data, self.stop = self.config()

    def test_draws_two_histograms(self):
        diff = cmpr.Comparator(stop=self.stop)

        self.data[2].SetTitle('Checking output ratio comparator')
        ratio = diff.compare(self.data[2], self.data[1])

        c1 = gcanvas()
        c1.SetLogy(0)
        self.assertIsNotNone(ratio)
        ratio.SetTitle("Test Output: This is output ratio plot")
        ratio.Draw()
        wait(stop=self.stop)

    def test_draws_multiple_histograms(self):
        diff = cmpr.Comparator(stop=self.stop)

        self.data[0].SetTitle('Checking output ratio comparator')
        self.assertTrue(
            all(diff.compare(arg) for arg in zip(*[self.data, self.data]))
        )
