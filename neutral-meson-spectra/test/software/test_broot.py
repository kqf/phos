#!/usr/bin/python

import ROOT
import unittest
import random
from spectrum.broot import Property
from spectrum.broot import BROOT as br
from spectrum.sutils import wait

class TestTH(unittest.TestCase):

    def setUp(self):
        self.hist = br.BH(ROOT.TH1F, "hist", "Testing creating of the histogram", 100, -10, 10,
            label = 'test')
        self.hist.FillRandom("gaus")
        self.properties = Property._properties.keys()


    def test_properties(self):
        for p in self.properties:
            self.assertTrue(p in dir(self.hist))


    def test_draw(self):
        self.assertIsNotNone(self.hist)
        self.hist.Draw()
        wait()

    def test_copy(self):
        histcopy = br.clone(self.hist, '')
        histcopy.SetBinContent(5,  1000)
        histcopy.Draw()
        self.hist.Draw('same')
        wait()


    @unittest.skip('Replace same_as with br.same static method')
    def test_set_properties(self):
        hist = br.BH(ROOT.TH1F, "refhistSet", "Testing set_property method", 100, -10, 10,
            label = "test prop", logy=True, logx=False, priority = 3)

        hist2 = br.clone(hist)

        # Properties should not copy when using copy constructor
        # NB: Is it neccessary? Yes!
        self.assertFalse(hist2.same_as(hist))

        ## Now copy the properties
        hist2.set_properties(hist, force = True)
        self.assertTrue(hist2.same_as(hist))


    def test_clone_from_root(self):
        hist = ROOT.TH1F("refhistROOT", "Testing set_property method", 100, -10, 10)

        hist2 = br.BH(ROOT.TH1F, hist)

        # Properties should not copy when using copy constructor
        #
        self.assertTrue(Property.has_properties(hist2))


    @unittest.skip('Replace same_as with br.same static method')
    def test_clone(self):
        hist = br.BH(ROOT.TH1F, "refhistClone", "Testing updated Clone method", 100, -10, 10,
            label = "test prop", logy=True, logx=False, priority = 3)

        self.hist.FillRandom("gaus")

        ## NB: There is no need to manually set properties
        hist2 = br.clone(hist)


        ## Copy differs from copy constructor
        self.assertTrue(hist.GetEntries() == hist2.GetEntries())


        ## Now copy the properties
        self.assertTrue(hist2.same_as(hist))


    @unittest.skip('Replace BHn classes with static methods')
    def test_bh2_projection(self):
        hist = BH2F("refhistProj",                              # Name
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
        wait()

        ## NB: There is no need to manually set properties
        hist2 = hist.ProjectionX('newname', 1, 50)


        ## Now copy the properties
        self.assertTrue(hist2.same_as(hist))
