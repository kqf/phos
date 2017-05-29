#!/usr/bin/python

import ROOT
import unittest
from spectrum.broot import BH1
from spectrum.sutils import wait

# TODO: add copy constructor

class TestTH(unittest.TestCase):

    def setUp(self):
        self.hist = BH1("hist", "Testing creating of the histogram", 100, -10, 10,
            label = 'test')
        self.hist.FillRandom("gaus")


    def testProperties(self):
        properties = ["label", "logy", "logx", "priority", "fitfunc"]
        for p in properties:
            self.assertTrue(p in dir(self.hist))


    def testDraw(self):
        self.assertIsNotNone(self.hist)
        self.hist.Draw()
        wait('')


    def testCopyConstructor(self):
        histcopy = BH1(self.hist)
        histcopy.SetBinContent(5,  1000)
        histcopy.Draw()
        self.hist.Draw('same')
        wait('')
