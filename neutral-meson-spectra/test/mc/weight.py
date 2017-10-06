#!/usr/bin/python

import sys
import unittest
import operator as op

import ROOT
from spectrum.spectrum import Spectrum
from spectrum.input import Input
from spectrum.sutils import gcanvas
from spectrum.options import Options
import spectrum.comparator as cmpr

from spectrum.broot import BROOT as br


# NB: MC generated pT spectrum differs from the real one
#     this should be taken into account as it might
#     affect the efficiency


class WeighMC(unittest.TestCase):

    def setUp(self):
        # Calculate the real data distribution
        #

        data = Input('LHC16', 'PhysOnlyTender'), Options('data', 'q')
        data = Spectrum(*data)
        self.data = br.scalew(data.evaluate().spectrum)

        # Calculate the same for productions
        inputs = Input('LHC16-old.root', 'PhysTender', 'MassPtN3'), Input('LHC16.root', 'PhysTender', 'MassPt')
        options = Options('old', 'q'),  Options('new', 'q')
        self.options_eta = Options('old', 'q', particle = 'eta'),  Options('new', 'q', particle = 'eta')
        self.stop = 'discover' not in sys.argv

        inputs = Input('Pythia-LHC16-a5', 'PhysNonlinOnlyTender'), #Input('LHC17d20a', 'PhysNonlinOnlyTender'), \
             # Input('pythia-jet-jet', 'PhysNonlinOnlyTender')

        options = Options('Pythia8', 'q', priority = 1), #Options('EPOS', 'q', priority = 99), \
            # Options('Pythia8 JJ', 'q', priority = 1)

        productions = [Spectrum(*pair) for pair in zip(inputs, options)]
        self.mcspectra = [br.scalew(s.evaluate().spectrum) for s in productions]
        self.mcspectra_gen = [br.scalew(s.evaluate().spectrum) for s in productions]


    def test_weights(self):
        for mc in self.mcspectra:
            self.data.fitfunc = self.fit_function()
            diff = cmpr.Comparator(stop = self.stop)
            diff.compare(self.data, mc)


    @staticmethod
    def fit_function():
        func_feeddown = ROOT.TF1("func_feeddown", "[2] * (1.+[0]*TMath::Exp(-x/2*x/2/2./[1]/[1]))", 0, 100);
        func_feeddown.SetParNames('A', '#sigma', 'Global Scale')
        func_feeddown.SetParameter(0, -1.057)
        func_feeddown.SetParameter(1, 0.814)
        func_feeddown.SetParameter(2, 0.6907)
        return func_feeddown

