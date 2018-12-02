import unittest
import sys

from spectrum.sutils import gcanvas
import spectrum.comparator as cmpr


class CheckDefault(unittest.TestCase):

    def setUp(self):
        self.discover = 'discover' in sys.argv
        self.mode = 'dead' if self.discover else 'q'
        self.canvas = gcanvas()

    def tearDown(self):
        if self.discover:
            return

        message = "Check your test case. It didn't produce any results"
        self.assertTrue(self.results, message)
        self.compare()

    def compare(self):
        diff = cmpr.Comparator()
        diff.compare(self.results)
