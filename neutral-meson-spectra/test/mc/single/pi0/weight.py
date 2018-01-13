#!/usr/bin/python

import sys
import unittest

import ROOT
from spectrum.input import Input
from spectrum.sutils import wait
from spectrum.options import Options
from spectrum.efficiency import EfficiencyMultirange
from spectrum.corrected_yield import CorrectedYield
from spectrum.sutils import gcanvas, adjust_canvas

import spectrum.comparator as cmpr
from spectrum.broot import BROOT as br
from test.mc.single.weight import WeighSingleParticleMC




# NB: The weighting from single particle MC differs, as 
#     the original shape of the distribution is flat. Therefore 
#     one can simply use different tsallist fits as weith function for
#     for flat p_T distribution


def corrected_spectrum(directory, join_point = 5):
        genhist = 'hPt_#pi^{0}_primary_'

        # Define inputs and options for different productions
        dinp, dopt = Input('LHC16', 'PhysOnlyTender', label='data'), Options('d')

        # SPMC
        inputs = {
            'single/{0}/LHC17j3b1'.format(directory): (0, join_point), 
            'single/{0}/LHC17j3b2'.format(directory): (join_point, 20)
        }

        eff = EfficiencyMultirange(
            genhist, 'eff', 
            inputs,
            selection = 'PhysEffOnlyTender'
        )

        return CorrectedYield(dinp, dopt, eff.eff())


class WeighSingleParticleEta(WeighSingleParticleMC):

    def setUp(self):
        self.stop = 'discover' not in sys.argv
        self.corrected_spectrum = corrected_spectrum

    @staticmethod
    def fit_function():
        tsallis =  ROOT.TF1("f", "x[0] * (x[0] )*[0]/2./3.1415*([2]-1.)*([2]-2.)/([2]*[1]*([2]*[1]+[4]*([2]-2.))) * (1.+(sqrt((x[0])*(x[0])+[3]*[3])-[4])/([2]*[1])) ** (-[2])", 0, 100);

        # No Weights
        # tsallis.SetParameters(2.4, 0.139, 6.880);

        # Weights0
        # tsallis.SetParameters(0.014948507575731244, 0.2874438247098432, 9.895472915554668)

        # Weights1
        tsallis.SetParameters(0.014960701090585591, 0.287830380417601, 9.921003040859755)
                             # [0.014850211992453644, 0.28695967166609104, 9.90060126848571        

        tsallis.FixParameter(3, 0.135);
        tsallis.FixParameter(4, 0.135);

        return tsallis
