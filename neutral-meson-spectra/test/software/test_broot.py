#!/usr/bin/python

import unittest
import sys
import os
import random

import ROOT

from spectrum.broot import BROOT as br
from spectrum.sutils import wait

# NB: Don't use broot in write functions
#     as it's important to test without broot
# 

def write_histogram(filename, selection, histname):
    hist = br.BH(ROOT.TH1F, histname, 'Testing reading ' + \
         'histograms from a rootfile', 10, -3, 3)
    hist.FillRandom('gaus')
    tlist = ROOT.TList()
    tlist.SetOwner(True)
    tlist.Add(hist)

    ofile = ROOT.TFile(filename, 'recreate')
    tlist.Write(selection, 1)
    ofile.Close()
    return br.clone(hist)

def write_histograms(filename, selection, histnames):
    hists = [br.BH(ROOT.TH1F, histname, 'Testing reading ' + 
                'histograms from a rootfile', 10, -3, 3) 
                for histname in histnames]

    for hist in hists:
        hist.FillRandom('gaus')

    tlist = ROOT.TList()
    tlist.SetOwner(True)
    map(tlist.Add, hists)

    ofile = ROOT.TFile(filename, 'recreate')
    tlist.Write(selection, 1)
    ofile.Close()
    return map(br.clone, hists)



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
            "refhistCopy", "Testing updated Clone method", 100, -10, 10,
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

    def test_bh2_draws_projection_range(self):
        hist = br.BH(ROOT.TH2F, "refhistProj",                  # Name
                    "Testing updated ProjectX method for BH2F", # Title
                    100, 20, 30, 100, -10, 10,                 # Xbins, Ybins
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
        hist2 = br.project_range(hist, 'newname', -5, 5)

        hist2.Draw()
        wait(draw = self.mode)

        ## Now copy the properties
        self.assertTrue(br.same(hist2, hist))

    def test_projection_saves_area(self):
        # NB: Bin according to this sequence https://oeis.org/A000124 
        #     so the bin width of a projection hist always increases
        #
        carter, ncarter = lambda n: n * (n + 1) / 2 + 1, 16

        # TODO: figure out what is why do we should nbinsx, not nbinsy
        #       this contradicts regular logic

        nbinsx, startx, stopx = carter(ncarter), -10, 10
        nbinsy, starty, stopy = 100, -10, 10

        hist = br.BH(ROOT.TH2F, "refhistProjArea",                # Name
                    "Testing updated ProjectX method for BH2F",   # Title
                    nbinsx, startx, stopx, nbinsy, starty, stopy, # Xbins, Ybins
                    label = "test prop",                          # Label
                    logy = 1, logx = 0, priority = 3              # Misc properties
                   )

        # Fill random values
        for i in range(1, hist.GetXaxis().GetNbins() + 1):
            for j in range(1, hist.GetYaxis().GetNbins() + 1):
                hist.SetBinContent(i, j, i * i * j * random.randint(1, 4))

        bin_edges = map(carter, range(ncarter))
        bins = zip(bin_edges[:-1], bin_edges[1:])

        projections = [br.projection(hist, "%d_%d", *bin) for bin in bins]

        # print 
        # for b, p in zip(bins, projections):
            # print b, p.Integral()
        print sum(p.Integral() for p in projections), hist.Integral()

        total = sum(p.Integral() for p in projections) 
        self.assertEqual(total, hist.Integral())

    def test_read(self):
        data = 'test_read.root', 'testSelection', 'testHistogram'
        write_histogram(*data)
        self.assertIsNotNone(br.io.read(*data))

        # Now raise exceptions when reading 
        # the root file with wrong names
        self.assertRaises(IOError, br.io.read, 'junk' + data[0], data[1], data[2])
        self.assertRaises(IOError, br.io.read, data[0], 'junk' + data[1], data[2])
        self.assertRaises(IOError, br.io.read, data[0], data[1], 'junk' + data[2])
        os.remove(data[0])

    def test_read_multiple(self):
        ofilename = 'test_read.root'
        selection = 'testSelection'
        histnames = ['testHistogram_{0}'.format(i) for i in range(10)]

        write_histograms(ofilename, selection, histnames)


        histograms = br.io.read_multiple(ofilename, selection, histnames)
        self.assertIsNotNone(histograms)
        self.assertEqual(len(histograms), len(histnames))
        self.assertIsNotNone(histograms[0])


        # Now feed it with wrong name 
        histnames.append('junk')
        self.assertRaises(IOError, br.io.read_multiple, 
            ofilename, selection, histnames)
        os.remove(ofilename)

    def test_ratio(self):
        hist1 = br.BH(ROOT.TH1F, 
            "refhistRatio1", "Testing the ratio method", 100, -10, 10,
            label = "test ratio", logy=True, logx=False, priority = 3)

        hist2 = br.BH(ROOT.TH1F, 
            "refhistRatio2", "Testing the ratio method", 100, -10, 10,
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
            "refhistSetEvents", "Testing set events", 100, -10, 10,
            label = "test ratio", logy=True, logx=False, priority = 3)

        hist1.FillRandom("gaus")
        events, integral = 1000, hist1.Integral()

        # No normalization
        br.set_nevents(hist1, events)

        # Check if .nevents attribute is OK
        self.assertEqual(hist1.nevents, events)
        # Check if we don't mess with area
        self.assertNotEqual(int(hist1.Integral()), int(integral / events))


        # Now with normalization
        br.set_nevents(hist1, events, True)
        # Check if .nevents attribute is OK
        self.assertEqual(hist1.nevents, events)
        # Check if we don't mess with area
        self.assertEqual(int(hist1.Integral()), int(integral / events))


    def test_rebins(self):
        hist1 = br.BH(ROOT.TH1F, 
            "refhistRebin1", "Testing rebins", 200, -10, 10,
            label = "test ratio", logy=True, logx=False, priority = 3)

        hist2 = br.BH(ROOT.TH1F, 
            "refhistRebin2", "Testing rebins", 100, -10, 10,
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
            "refhistSum_%d" % i, "Testing sum %d" % i, 200, -10, 10,
            label = "%dth histogram" % i, logy=True, logx=False, priority = 3)
            for i in range(10)]

        for hist in hists:
            hist.FillRandom('gaus')

        entries = sum(h.GetEntries() for h in hists)

        newlabel = 'total'
        total = br.sum(hists, newlabel)

        self.assertEqual(total.GetEntries(), entries)
        self.assertEqual(total.label, newlabel)


    def test_scales_histogram(self):
        nbins, start, stop =  200, -10, 10

        hist = br.BH(ROOT.TH1F, 
            "refhistScale", "Testing scalew", nbins, start, stop,
            label = "scale", logy=True, logx=False, priority = 3)

        hist.FillRandom('gaus')

        # Calculate bin width
        binwidth = nbins * 1./ (stop - start)

        # For normal even binning these numbers are the same
        entries, integral = hist.GetEntries(), hist.Integral()
        self.assertEqual(entries, integral)

        br.scalew(hist, 1)
        self.assertEqual(entries, hist.GetEntries())
        self.assertEqual(hist.Integral(), integral * binwidth)

        # NB: Be careful when applying scalew consecutively
        #     the factors multiply
        br.scalew(hist, 2)
        self.assertEqual(entries, hist.GetEntries())
        self.assertEqual(hist.Integral(), integral * binwidth * binwidth * 2)


    def test_calculates_area_and_error(self):
        nbins, start, stop = 10, 0, 10
        hist = br.BH(ROOT.TH1F, 
            "refhistAreaError", "Testing area and error", nbins, start, stop,
            label = "scale", logy=True, logx=False, priority = 3)

        for i in range(nbins):
            hist.Fill(i, i)


        triangle = lambda n: n * (n - 1) / 2
        farea = lambda a, b: triangle(b) - triangle(a)

        # These areas work according to the formula
        test_areas = (0, 10), (5, 10), (0, 0)
        for interval in test_areas:
            area, error = br.area_and_error(hist, *interval)

            true = farea(*interval)

            self.assertEqual(area, true)
            self.assertEqual(error, true ** 0.5)

        # NB: ROOT behaviour
        # But these areas don't work according agree with expectations
        # because ROOT takes into account both ends of the interval
        fail_areas =  (5, 6), (0, 1), (1, 8)
        for interval in fail_areas:
            area, error = br.area_and_error(hist, *interval)
            true = farea(*interval)

            self.assertNotEqual(area, true)
            # There is no need to compare errors

    def test_rebins_for_given_ranges(self):
        nbins, start, stop =  200, -10, 10

        new_edges = [-10, -3, -2, 0, 1, 4, 6, 10]
        newbins = zip(new_edges[:-1], new_edges[1:])

        hist = br.BH(ROOT.TH1F, 
            "refhistEdges", "Testing scalew", nbins, start, stop,
            label = "scale", logy=True, logx=False, priority = 3)
        hist.FillRandom('gaus')

        rebinned = br.rebin(hist, new_edges)
        self.assertEqual(hist.Integral(), rebinned.Integral())
        self.assertEqual(hist.GetEntries(), rebinned.GetEntries())
        self.assertTrue(br.same(hist, rebinned))
        self.assertEqual(rebinned.GetNbinsX(), len(newbins))

        for i, bin in enumerate(newbins):
            binw = bin[1] - bin[0]
            self.assertEqual(rebinned.GetBinWidth(i + 1), binw)


    def test_saves_histogram(self):
        oname, selection, histname = 'testSave.root', 'testSelection', 'refhistSave'
        hist = br.BH(ROOT.TH1F, 
            histname, "Testing scalew", 200, -10, 10,
            label = "scale", logy=True, logx=False, priority = 3)
        hist.FillRandom('gaus')
        integral = hist.Integral()
        entries = hist.GetEntries()


        br.io.save(hist, oname, selection)
        self.assertTrue(os.path.isfile(oname))

        ffile = br.io.read(oname, selection, histname)
        self.assertEqual(ffile.GetEntries(), entries)
        self.assertEqual(ffile.Integral(), integral)
        os.remove(oname)




