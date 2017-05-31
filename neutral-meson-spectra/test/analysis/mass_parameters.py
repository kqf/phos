#!/usr/bin/python

from spectrum.spectrum import Spectrum
from spectrum.ptanalyzer import PtDependent
from spectrum.options import Options
from spectrum.input import Input, read_histogram
from spectrum.sutils import get_canvas, adjust_canvas
from spectrum.sutils import wait
from spectrum.comparator import Comparator
from spectrum.sutils import save_tobject

import ROOT

import os.path
import unittest


# TODO: Merge this method with width/mass parametrization

class TestMassParameters(unittest.TestCase):


    def get_analysis(self, iname):
        return Spectrum(Input(iname, 'PhysNonlinTender').read())


    def read_histograms(self, infile):
        return [i.ReadObj() for i in infile.GetListOfKeys()]


    def data(self, iname, oname):
        infile = ROOT.TFile(oname)
        if infile.IsOpen():
            return self.read_histograms(infile)


        f = self.get_analysis(iname)
        mass, sigma = f.analyzer.quantities(False)[0:2]
        save_tobject(mass, oname, 'recreate')
        save_tobject(sigma, oname, 'update')
        # TODO: Finish this code, add fitters


        return mass, sigma

    def testMass(self):
        mass, sigmma = self.data('input-data/Pythia-LHC16-iteration16.root', 'mass-Pythia-LHC16-iteration16.root')

