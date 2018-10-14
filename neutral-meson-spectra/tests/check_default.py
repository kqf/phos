#!/usr/bin/python
import unittest
import ROOT
import sys

from spectrum.sutils import gcanvas

class CheckDefault(unittest.TestCase):

    def setUp(self):
        self.discover = 'discover' in sys.argv
        self.mode = 'dead' if self.discover else 'q'
        self.canvas = gcanvas() 

    def tearDown(self):
        if self.discover:
            return

        self.assertTrue(self.results, "Check your test case. It didn't produce any results")
        self.compare()

    def compare(self):
        import spectrum.comparator as cmpr
        diff = cmpr.Comparator()
        diff.compare(self.results)
