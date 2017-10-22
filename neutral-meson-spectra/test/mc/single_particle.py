#!/usr/bin/python

from spectrum.spectrum import Spectrum
from spectrum.options import Options
from spectrum.input import Input, read_histogram
from spectrum.comparator import Comparator


from spectrum.broot import BROOT as br

from test.analysis.test_check_different_modules import run_analysis

import ROOT

import os.path
import unittest


class SingleParticleQA(unittest.TestCase):


    def particle_ptbin(self, prod):
        name, bin = prod[:-1], prod[-1]
        return self.simulation.get(name), self.ptbin.get(bin)


    def setUp(self):
        # Dataset description
        #
        self.simulation = {'LHC17j3a': '#gamma', 'LHC17j3b': '#pi^{0}', 'LHC17j3c': '#eta'}
        self.ptbin  = {'1': 'low p_{T}', '2': 'high p_{T}'}

        # Define input
        self.selection = 'MCStudyOnlyTender'
        self.productions = 'LHC17j3b2', 'LHC17j3a2'


    def test_pt_generated(self):
        for prod in self.productions:
            etaphi = self.distribution(prod, 'hEtaPhi_{0}')
            diff = Comparator()
            diff.compare(etaphi)


    def test_eta_phi_distribution(self):
        for prod in self.productions:
            etaphi = self.distribution(prod, 'hPt_{0}_primary_')
            diff = Comparator()
            diff.compare(etaphi)


    def distribution(self, filename, histname):
        part, ptbin = self.particle_ptbin(filename)
        label = '{0} {1}'.format(part, ptbin)
        hist = read_histogram(filename, self.selection,\
            histname.format(part), label = label)

        br.scalew(hist)
        return hist 

