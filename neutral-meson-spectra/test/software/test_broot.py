#!/usr/bin/python

import ROOT
import unittest
from spectrum.broot import BH1
from spectrum.sutils import wait

class TestTH(unittest.TestCase):

    def setUp(self):
        self.hist = BH1("hist", "Testing creating of the histogram", 100, -10, 10,
            label = 'test')
        self.hist.FillRandom("gaus")


    @unittest.skip('')
    def testProperties(self):
        properties = ["label", "logy", "logx", "priority", "fitfunc"]
        for p in properties:
            self.assertTrue(p in dir(self.hist))


    @unittest.skip('')
    def testDraw(self):
        self.assertIsNotNone(self.hist)
        self.hist.Draw()
        wait('')


    @unittest.skip('')
    def testCopyConstructor(self):
        histcopy = BH1(self.hist)
        histcopy.SetBinContent(5,  1000)
        histcopy.Draw()
        self.hist.Draw('same')
        wait('')


    def testSetProperties(self):
        hist = BH1("refhist", "Testing set_property method", 100, -10, 10,
            label = "test prop", logy=True, logx=False, priority = 3)

        hist2 = BH1(hist)

        # Properties should not copy when using copy constructor
        # TODO: Is it neccessary?
        self.assertFalse(hist2.label == hist.label)

        print
        print 'label', hist2.label

        ## Now copy the properties
        hist2.set_properties(hist)
        print 'label', hist2.label
        self.assertTrue(hist2.label == hist.label)

