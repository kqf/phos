#!/usr/bin/python

import sys
import unittest

import ROOT
from spectrum.input import Input
from spectrum.sutils import wait
from spectrum.options import Options
from spectrum.efficiency import EfficiencyMultirange
from spectrum.corrected_yield import CorrectedYield

import spectrum.comparator as cmpr
from spectrum.broot import BROOT as br



# NB: The weighting from single particle MC differs, as 
#     the original shape of the distribution is flat. Therefore 
#     one can simply use different tsallist fits as weith function for
#     for flat p_T distribution

class WeighSingleParticleMC(unittest.TestCase):

    def setUp(self):
        genhist = 'hPt_#pi^{0}_primary_'
        self.stop = 'discover' not in sys.argv

        # Define inputs and options for different productions
        dinp, dopt = Input('LHC16', 'PhysOnlyTender'), Options('data', 'q')

        # SPMC
        inputs = {
            'single/weight0/LHC17j3b1': (0, 7), 
            'single/weight0/LHC17j3b2': (7, 20)
        }

        eff = EfficiencyMultirange(
            genhist, 'eff', 
            inputs,
            selection = 'PhysEffOnlyTender'
        )

        self.corrected_spectrum = CorrectedYield(dinp, dopt, eff.eff())


    def test_weights(self):
        fitf = self.fit_function()
        cyield = self.corrected_spectrum.evaluate()
        cyield.Fit(fitf)
        cyield.Draw()
        ROOT.gPad.SetLogx()
        ROOT.gPad.SetLogy()
        wait()
        

    @staticmethod
    def fit_function():
        tsallis =  ROOT.TF1("f", "x[0] * (x[0] )*[0]/2./3.1415*([2]-1.)*([2]-2.)/([2]*[1]*([2]*[1]+[4]*([2]-2.))) * (1.+(sqrt((x[0])*(x[0])+[3]*[3])-[4])/([2]*[1])) ** (-[2])", 0, 100);
        tsallis.SetParameters(2.4, 0.139, 6.880);
        tsallis.FixParameter(3, 0.135);
        tsallis.FixParameter(4, 0.135);
        return tsallis

