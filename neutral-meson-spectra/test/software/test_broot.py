#!/usr/bin/python

import unittest
import sys
import random

import ROOT

from spectrum.broot import BROOT as br
from spectrum.sutils import wait

def write_histogram(filename, selection, histname):
    hist = ROOT.TH1F(histname, 'Testing reading ' + \
         'histograms from a rootfile', 10, -3, 3)
    tlist = ROOT.TList()
    tlist.SetOwner(True)
    tlist.Add(hist)

    ofile = ROOT.TFile(filename, 'recreate')
    tlist.Write(selection, 1)
    ofile.Close()



class TestTH(unittest.TestCase):

    def setUp(self):
        self.mode = 'discover' not in sys.argv
        self.mode = 'discover' in sys.argv
        self.hist = br.BH(ROOT.TH1F, "hist" + str(random.randint(0, 1e9)), 
            "Testing creating of the histogram", 100, -10, 10,
            label = 'test')
        self.hist.FillRandom("gaus")
        self.properties = br.prop._properties.keys()


    def test_properties(self):
        for p in self.properties:
            self.assertTrue(p in dir(self.hist))


    def test_draw(self):
        self.assertIsNotNone(self.hist)
        self.hist.Draw()
        wait(draw = self.mode)


    def test_setp(self):
        hist = ROOT.TH1F("refhistSet", "Testing set_property method", 100, -10, 10)

        # Set properties of root object
        br.setp(hist, self.hist)

        self.assertTrue(br.same(hist, self.hist))


    def test_clone_from_root(self):
        hist = br.BH(ROOT.TH1F, "refhistROOT", "Testing set_property method", 100, -10, 10)

        hist2 = br.BH(ROOT.TH1F, hist)

        # Properties should not copy when using copy constructor
        #
        self.assertTrue(br.prop.has_properties(hist2))



    def test_clone(self):
        hist = br.BH(ROOT.TH1F, "refhistClone", "Testing updated Clone method", 100, -10, 10,
            label = "test prop", logy=True, logx=False, priority = 3)

        hist.FillRandom("gaus")

        ## NB: There is no need to manually set properties
        hist2 = br.clone(hist)

        ## Copy differs clone
        self.assertTrue(hist.GetEntries() == hist2.GetEntries())

        ## Now copy the properties
        self.assertTrue(br.same(hist2, hist))


    def test_copy(self):
        hist = br.BH(ROOT.TH1F, "refhistClone", "Testing updated Clone method", 100, -10, 10,
            label = "test prop", logy=True, logx=False, priority = 3)

        hist.FillRandom("gaus")

        ## NB: There is no need to manually set properties
        ## Now try copy instead of clone
        hist2 = br.copy(hist)

        ## Copy differs clone
        ## These should not equal
        self.assertFalse(hist.GetEntries() == hist2.GetEntries()) 

        ## Now copy the properties
        self.assertTrue(br.same(hist2, hist))


    def test_clone_visual(self):
        histcopy = br.clone(self.hist, '')
        histcopy.SetBinContent(5,  1000)
        histcopy.Draw()
        self.hist.Draw('same')
        wait(draw = self.mode)

    def test_bh2_projection(self):
        hist = br.BH(ROOT.TH2F, "refhistProj",                  # Name
                    "Testing updated ProjectX method for BH2F", # Title
                    100, -10, 10, 100, -10, 10,                 # Xbins, Ybins
                    label = "test prop",                        # Label
                    logy = 1, logx = 0, priority = 3            # Misc properties
                   )

        # Fill random values
        for i in range(1, hist.GetXaxis().GetNbins() + 1):
            for j in range(1, hist.GetYaxis().GetNbins() + 1):
                hist.SetBinContent(i, j, i * i * j * random.randint(1, 4))

 
        hist.Draw('colz')
        wait(draw = self.mode)

        ## NB: There is no need to manually set properties
        hist2 = br.projection(hist, 'newname', 1, 50)

        hist2.Draw()
        wait(draw = self.mode)

        ## Now copy the properties
        self.assertTrue(br.same(hist2, hist))


    def test_read(self):
        data = 'test_read.root', 'testSelection', 'testHistogram'
        write_histogram(*data)
        self.assertIsNotNone(br.read.read(*data))

        # Now raise exceptions when reading 
        # the root file with wrong names
        self.assertRaises(IOError, br.read.read, 'junk' + data[0], data[1], data[2])
        self.assertRaises(IOError, br.read.read, data[0], 'junk' + data[1], data[2])
        self.assertRaises(IOError, br.read.read, data[0], data[1], 'junk' + data[2])
