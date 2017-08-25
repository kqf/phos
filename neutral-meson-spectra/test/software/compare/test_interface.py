import unittest
import spectrum.comparator as cmpr
from particles import Particles

class TestComparatorInterface(unittest.TestCase, Particles):

    def setUp(self):
        self.data = self.config()

    def testCompareOK(self):
        diff = cmpr.Comparator()
        for d in self.data: d.SetTitle('Compare coma separated arguments')
        diff.compare(*self.data)

        for d in self.data: d.SetTitle('Compare a single list of arguments')
        diff.compare(self.data)

        for d in self.data: d.SetTitle('Compare two lists of arguments')
        diff.compare(self.data, self.data[::-1])

        for d in self.data: d.SetTitle('Compare set of arguments')
        diff.compare(zip(*[self.data, self.data]))

    def testCompareFail(self):
        diff = cmpr.Comparator()
        for d in self.data: d.SetTitle('Fail')

        with self.assertRaises(AssertionError):
            diff.compare(self.data, [[0]])

