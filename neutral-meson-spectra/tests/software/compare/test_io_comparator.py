import ROOT
import unittest
import os
from spectrum.comparator import Comparator
from particles import Particles
import spectrum.sutils as su


class TestComparator(unittest.TestCase, Particles):

    def setUp(self):
        self.data, self.stop = self.config()
        self.fname = "test_io_deleteme.root"

    def testCompareMultiple(self):
        ofile = ROOT.TFile(self.fname, "recreate")
        ofile.mkdir("test1/test2/")
        Comparator(stop=self.stop).compare(self.data)
        ofile.cd("test1/test2/")
        su.gcanvas().Write()
        ofile.Write()

    def tearDown(self):
        infile = ROOT.TFile(self.fname)
        infile.ls()
        os.remove(self.fname)
