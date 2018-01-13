#!/usr/bin/python

import sys
import unittest
import operator as op

import ROOT
from spectrum.spectrum import Spectrum
from spectrum.input import Input
from spectrum.sutils import gcanvas, wait
from spectrum.options import Options
from spectrum.efficiency import Efficiency, EfficiencyMultirange
from spectrum.corrected_yield import CorrectedYield
import spectrum.comparator as cmpr

from spectrum.broot import BROOT as br


# NB: MC generated pT spectrum differs from the real one
#     this should be taken into account as it might
#     affect the efficiency


class WeighGeneralPurposeMC(unittest.TestCase):

    def setUp(self):
        genhist = 'hPt_#pi^{0}_primary_'
        self.stop = 'discover' not in sys.argv

        # Define inputs and options for different productions
        dinp, dopt = Input('LHC16', 'PhysOnlyTender', label='data'), Options('q')

        # 
        inputs = Input('Pythia-LHC16-a5', 'PhysNonlinOnlyTender'), #Input('LHC17d20a', 'PhysNonlinOnlyTender'), \
        eff = [Efficiency(genhist, 'eff', i.filename) for i in inputs]

        self.productions = [CorrectedYield(dinp, dopt, e.eff()) for e in eff]
        self.mcgenerated = [e.true() for e in eff]


    def test_weights(self):
        corrected_spectra = [cy.evaluate() for cy in self.productions]
        for spectrum, mc in zip(corrected_spectra, self.mcgenerated):
            spectrum.fitfunc = self.fit_function()
            diff = cmpr.Comparator(stop = self.stop)
            diff.compare(spectrum, mc)


    @staticmethod
    def fit_function():
        func_feeddown = ROOT.TF1("func_feeddown", "[2] * (1.+[0]*TMath::Exp(-x/2*x/2/2./[1]/[1]))", 0, 100);
        func_feeddown.SetParNames('A', '#sigma', 'scale')
        func_feeddown.SetParameter(0, -1.063)
        func_feeddown.SetParameter(1, 0.855)
        func_feeddown.SetParameter(2, 2.0)
        return func_feeddown

