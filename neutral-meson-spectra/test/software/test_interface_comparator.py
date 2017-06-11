
import unittest
import ROOT
import json


import spectrum.comparator as cmpr
from test.software.test_compare import get_spectrum

class TestComparatorInterface(unittest.TestCase):

    def setUp(self):
        with open('config/test_particles.json') as f: 
            particles = json.load(f)
        self.data = [get_spectrum(i, *particles[i]) for i in particles]

    # @unittest.skip('test')
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

