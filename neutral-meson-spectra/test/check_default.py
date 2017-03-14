#!/usr/bin/python
import unittest
import ROOT
import sys

from spectrum.sutils import get_canvas

class CheckDefault(unittest.TestCase):

    def setUp(self):
        self.discover = 'discover' in sys.argv
        self.mode = 'dead' if self.discover else 'q'
        self.canvas = get_canvas() 

    def tearDown(self):
        if self.discover:
            return

        self.assertTrue(self.results, "Check your test case. It didn't produce any results")
        self.compare()

    def compare(self):
        import spectrum.comparator as cmpr
        diff = cmpr.Comparator()
        diff.compare_set_of_histograms(self.results)
