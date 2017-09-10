import unittest

import spectrum.comparator as cmpr
from spectrum.sutils import wait, gcanvas
from particles import Particles

class TestOutputRatio(unittest.TestCase, Particles):
    """
         This test is needed to check if comparator returns ratio histogram correctly
         or none object when it's not relevant.
    """


    def setUp(self):
        self.data = self.config()


    def testCompareTwo(self):
        diff = cmpr.Comparator()

        self.data[2].SetTitle('Checking output ratio comparator')
        ratio = diff.compare(self.data[2], self.data[1])

        c1 = gcanvas()
        c1.SetLogy(0)
        if ratio:
            ratio.Draw()

        wait("test", True, False)


    def testCompareMultiple(self):
        diff = cmpr.Comparator()

        self.data[0].SetTitle('Checking output ratio comparator')
        ratio = diff.compare(zip(*[self.data, self.data]))
        self.assertFalse(all(ratio))




