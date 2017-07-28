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
        return Spectrum(Input(iname, 'PhysNonlinTender', 'MassPt').read())


    def read_histograms(self, infile):
        return [i.ReadObj() for i in infile.GetListOfKeys()]


    def data(self, f, oname):
        infile = ROOT.TFile(oname)
        if infile.IsOpen():
            return self.read_histograms(infile)

        mass, sigma = f.analyzer.quantities(False)[0:2]
        save_tobject(mass, oname, 'recreate')
        save_tobject(sigma, oname, 'update')
        return mass, sigma

    def testMass(self):
        iname = 'input-data/Pythia-LHC16-a5.root'
        fs = self.get_analysis(iname)
        mass, sigmma = self.data(fs, 'mass-' + iname)

        pars = [-4.13409, -1.4885, 6.26014, 0.1378]
        fitmass = fs.fit_quantity(mass, fs.mass_func, pars, fs.mass_names, 'mass')
        print fs.mass_pars

