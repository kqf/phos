#!/usr/bin/python

import unittest
import sys
import os
import random
from math import ceil

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

def write_histograms(filename, selection, histnames):
    hists = [ROOT.TH1F(histname, 'Testing reading ' + 
                'histograms from a rootfile', 10, -3, 3) 
                for histname in histnames]

    tlist = ROOT.TList()
    tlist.SetOwner(True)
    map(tlist.Add, hists)

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
        hist = ROOT.TH1F("refhistSet", "Testing set_property method",
            100, -10, 10)

        # Set properties of root object
        br.setp(hist, self.hist)

        self.assertTrue(br.same(hist, self.hist))


    def test_clone_from_root(self):
        hist = br.BH(ROOT.TH1F, "refhistROOT", "Testing set_property method", 
            100, -10, 10)

        hist2 = br.BH(ROOT.TH1F, hist)

        # Properties should not copy when using copy constructor
        #
        self.assertTrue(br.prop.has_properties(hist2))



    def test_clone(self):
        hist = br.BH(ROOT.TH1F, 
            "refhistClone", "Testing updated Clone method", 100, -10, 10,
            label = "test prop", logy=True, logx=False, priority = 3)

        hist.FillRandom("gaus")

        ## NB: There is no need to manually set properties
        hist2 = br.clone(hist)

        ## Copy differs clone
        self.assertTrue(hist.GetEntries() == hist2.GetEntries())

        ## Now copy the properties
        self.assertTrue(br.same(hist2, hist))


    def test_copy(self):
        hist = br.BH(ROOT.TH1F, 
            "refhistClone", "Testing updated Clone method", 100, -10, 10,
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
        os.remove(data[0])

    def test_read_multiple(self):
        ofilename = 'test_read.root'
        selection = 'testSelection'
        histnames = ['testHistogram_{0}'.format(i) for i in range(10)]

        write_histograms(ofilename, selection, histnames)


        histograms = br.read.read_multiple(ofilename, selection, histnames)
        self.assertIsNotNone(histograms)
        self.assertEqual(len(histograms), len(histnames))
        self.assertIsNotNone(histograms[0])


        # Now feed it with wrong name 
        histnames.append('junk')
        self.assertRaises(IOError, br.read.read_multiple, 
            ofilename, selection, histnames)
        os.remove(ofilename)

    def test_ratio(self):
        hist1 = br.BH(ROOT.TH1F, 
            "refhistClone", "Testing the ratio method", 100, -10, 10,
            label = "test ratio", logy=True, logx=False, priority = 3)

        hist2 = br.BH(ROOT.TH1F, 
            "refhistClone", "Testing the ratio method", 100, -10, 10,
            label = "test ratio b", logy=True, logx=False, priority = 3)

        hist1.FillRandom("gaus")
        hist1.FillRandom("expo")
        ratio = br.ratio(hist1, hist2)

        # Check if the numerator and the ratio are the same
        self.assertTrue(br.same(hist1, ratio))

        # Check if the numerator and the ratio are not same
        self.assertFalse(br.same(hist2, ratio))

    def test_sets_events(self):
        hist1 = br.BH(ROOT.TH1F, 
            "refhistClone", "Testing set events", 100, -10, 10,
            label = "test ratio", logy=True, logx=False, priority = 3)

        hist1.FillRandom("gaus")
        events, integral = 1000, hist1.Integral()

        # No normalization
        br.set_nevents(hist1, events)

        # Check if .nevents attribute is OK
        self.assertEqual(hist1.nevents, events)
        # Check if we don't mess with area
        self.assertNotEqual(ceil(hist1.Integral()), ceil(integral / events))

        # Now with normalization

        br.set_nevents(hist1, events, True)
        # Check if .nevents attribute is OK
        self.assertEqual(hist1.nevents, events)
        # Check if we don't mess with area
        self.assertEqual(ceil(hist1.Integral()), ceil(integral / events))


    def test_rebins(self):
        hist1 = br.BH(ROOT.TH1F, 
            "refhistClone", "Testing rebins", 200, -10, 10,
            label = "test ratio", logy=True, logx=False, priority = 3)

        hist2 = br.BH(ROOT.TH1F, 
            "refhistClone", "Testing rebins", 100, -10, 10,
            label = "test ratio", logy=True, logx=False, priority = 3)

        hist1.FillRandom("gaus")
        hist2.FillRandom("gaus")

        rebinned, hist2 = br.rebin_as(hist1, hist2)

        self.assertNotEqual(hist1.GetNbinsX(), hist2.GetNbinsX())

        self.assertEqual(rebinned.GetNbinsX(), hist2.GetNbinsX())

        # Just check if ratio gives warnings
        ratio = br.ratio(rebinned, hist2)
        self.assertTrue(br.same(rebinned, hist1))


    def test_sum(self):
        hists = [ br.BH(ROOT.TH1F, 
            "refhistClone_%d" % i, "Testing sum %d" % i, 200, -10, 10,
            label = "%dth histogram" % i, logy=True, logx=False, priority = 3)
            for i in range(10)]

        for hist in hists:
            hist.FillRandom('gaus')

        entries = sum(h.GetEntries() for h in hists)

        newlabel = 'total'
        total = br.sum(hists, newlabel)

        self.assertEqual(total.GetEntries(), entries)
        self.assertEqual(total.label, newlabel)














