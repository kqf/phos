import ROOT
import unittest
from spectrum.comparator import Comparator
from particles import Particles


class TestComparator(unittest.TestCase, Particles):

    def test(self):
        hist = ROOT.TH2F('h', 'h', 20, 0, 5, 20, 0, 5)
        for i in range(1, 5):
            for j in range(1, 5):
                hist.Fill(i, j, i)
        Comparator().compare(hist)
        hist.Draw()
