#!/usr/bin/python

import ROOT
import unittest
import random
from spectrum.broot import BH1F, BH2F, Property
from spectrum.sutils import wait

class TestTH(unittest.TestCase):

    def setUp(self):
        self.hist = BH1F("hist", "Testing creating of the histogram", 100, -10, 10,
            label = 'test')
        self.hist.FillRandom("gaus")


    def testProperties(self):
        properties = ["label", "logy", "logx", "priority", "fitfunc"]
        for p in properties:
            self.assertTrue(p in dir(self.hist))


    def testDraw(self):
        self.assertIsNotNone(self.hist)
        self.hist.Draw()
        wait()


    def testCopyConstructor(self):
        histcopy = BH1F(self.hist)
        histcopy.SetBinContent(5,  1000)
        histcopy.Draw()
        self.hist.Draw('same')
        wait()


    def testSetProperties(self):
        hist = BH1F("refhistSet", "Testing set_property method", 100, -10, 10,
            label = "test prop", logy=True, logx=False, priority = 3)

        hist2 = BH1F(hist)

        # Properties should not copy when using copy constructor
        # TODO: Is it neccessary?
        self.assertFalse(hist2.same_as(hist))

        ## Now copy the properties
        hist2.set_properties(hist)
        self.assertTrue(hist2.same_as(hist))


    def testCloneFromROOT(self):
        hist = ROOT.TH1F("refhistROOT", "Testing set_property method", 100, -10, 10)

        hist2 = BH1F(hist)

        # Properties should not copy when using copy constructor
        #
        self.assertTrue(Property.has_properties(hist2))


    def testClone(self):
        hist = BH1F("refhistClone", "Testing updated Clone method", 100, -10, 10,
            label = "test prop", logy=True, logx=False, priority = 3)

        self.hist.FillRandom("gaus")

        ## NB: There is no need to manually set properties
        hist2 = hist.Clone()


        ## Copy differs from copy constructor
        self.assertTrue(hist.GetEntries() == hist2.GetEntries())


        ## Now copy the properties
        self.assertTrue(hist2.same_as(hist))


    def testBH2FProjection(self):
        hist = BH2F("refhistProj", "Testing updated ProjectX method for BH2F", 100, -10, 10, 100, -10, 10,
            label = "test prop", logy=True, logx=False, priority = 3)

        # Fill random values
        for i in range(1, hist.GetXaxis().GetNbins() + 1):
            for j in range(1, hist.GetYaxis().GetNbins() + 1):
                hist.SetBinContent(i, j, i * i * j * random.randint(1, 4))

 
        hist.Draw('colz')
        wait()

        ## NB: There is no need to manually set properties
        hist2 = hist.ProjectionX('newname', 1, 50)


        ## Now copy the properties
        self.assertTrue(hist2.same_as(hist))
