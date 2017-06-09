#!/usr/bin/python

import ROOT
import unittest
import random
from spectrum.broot import BH1, BH2
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


    @unittest.skip('')
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


    @unittest.skip('')
    def testCloneFromROOT(self):
        hist = ROOT.TH1F("refhist", "Testing set_property method", 100, -10, 10)

        hist2 = BH1(hist)

        # Properties should not copy when using copy constructor
        #
        self.assertTrue('label' in dir(hist2))
        self.assertTrue('logy' in dir(hist2))
        self.assertTrue('priority' in dir(hist2))
        self.assertTrue('fitfunc' in dir(hist2))


    @unittest.skip('')
    def testClone(self):
        hist = BH1("refhist", "Testing updated Clone method", 100, -10, 10,
            label = "test prop", logy=True, logx=False, priority = 3)

        self.hist.FillRandom("gaus")

        ## NB: There is no need to manually set properties
        hist2 = hist.Clone()


        ## Copy differs from copy constructor
        self.assertTrue(hist.GetEntries() == hist2.GetEntries())


        ## Now copy the properties
        self.assertTrue(hist2.label == hist.label)


    def testBH2Projection(self):
        hist = BH2("refhist", "Testing updated ProjectX method", 100, -10, 10, 100, -10, 10,
            label = "test prop", logy=True, logx=False, priority = 3)

        for i in range(1, hist.GetXaxis().GetNbins() + 1):
            for j in range(1, hist.GetYaxis().GetNbins() + 1):
                hist.SetBinContent(i, j, i * i * j * random.randint(1, 4))

 
        hist.Draw('colz')
        raw_input()

        ## NB: There is no need to manually set properties
        hist2 = hist.ProjectionX('newname', 1, 50)


        ## Copy differs from copy constructor
        # self.assertTrue(hist.GetEntries() == hist2.GetEntries())


        ## Now copy the properties
        self.assertTrue('label' in dir(hist2))

