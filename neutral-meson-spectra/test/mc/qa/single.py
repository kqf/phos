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

        if bin not in self.ptbin:
            name, bin = prod, ''

        return self.simulation.get(name), self.ptbin.get(bin)

    def setUp(self):
        # Dataset description
        #
        # NB: Always use unscaled version for QA
        self.dir = 'single/plain/'
        self.simulation = {'LHC17j3a': '#gamma', 'LHC17j3b': '#pi^{0}',
                           'LHC17j3c': '#eta', 'scaled-LHC17j3b': '#pi^{0}'}
        self.ptbin = {'1': 'low p_{T}', '2': 'high p_{T}', '': 'all'}

        # Define input
        self.selection = 'MCStudyOnlyTender'
        self.productions = 'LHC17j3a2', 'LHC17j3c2', 'LHC17j3b1', 'LHC17j3a1', 'LHC17j3c1'

    def test_pt_reconstructed(self):
        for prod in self.productions:
            reco = self.reconstructed(prod)
            diff = Comparator(oname=prod + '_reco')
            diff.compare(reco)

    # @unittest.skip('')
    def test_pt_generated(self):
        for prod in self.productions:
            pt = self.distribution(prod, 'hEtaPhi_{0}', 0)
            diff = Comparator(oname=prod + '_yphi')
            diff.compare(pt)

    # @unittest.skip('')
    def test_eta_phi_distribution(self):
        for prod in self.productions:
            etaphi = self.distribution(prod, 'hPt_{0}_primary_')
            diff = Comparator(oname=prod + '_pt')
            diff.compare(etaphi)

    def distribution(self, filename, histname, logy=1):
        part, ptbin = self.particle_ptbin(filename)
        label = '{0} {1}'.format(part, ptbin)
        hist = read_histogram(self.dir + filename, self.selection,
                              histname.format(part), label=label)
        hist.SetTitle(hist.GetTitle() + ', ' + ptbin)

        hist.logy = logy
        br.scalew(hist)
        return hist

    def reconstructed(self, filename):
        part, ptbin = self.particle_ptbin(filename)

        # NB: Gamma Follows different procedure
        if 'gamma' in part:
            hist = self.distribution(filename, 'hPt_{0}')
            hist.SetTitle('Inclusive ' + hist.GetTitle().lower())
            return hist

        return self._reconstructed(filename)

    def _reconstructed(self, filename):
        part, ptbin = self.particle_ptbin(filename)
        label = '{0} {1}'.format(part, ptbin)

        inp = Input(self.dir + filename, self.selection, label=label)
        opt = Options(mode='d', particle='pi0' if 'pi' in part else 'eta')
        reco = Spectrum(inp, opt).evaluate().spectrum
        reco.SetTitle(reco.GetTitle() + ', ' + ptbin)
        br.scalew(reco)
        return reco
