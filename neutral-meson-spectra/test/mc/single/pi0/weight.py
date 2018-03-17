#!/usr/bin/python

import sys
import unittest

import ROOT
from spectrum.input import Input
from spectrum.sutils import wait
from spectrum.options import Options, MultirangeEfficiencyOptions
from spectrum.efficiency import EfficiencyMultirange
from spectrum.corrected_yield import CorrectedYield
from spectrum.output import AnalysisOutput
import spectrum.sutils as su

import spectrum.comparator as cmpr
from spectrum.broot import BROOT as br
from test.mc.single.weight import WeighSingleParticleMC

from vault.datavault import DataVault




# NB: The weighting from single particle MC differs, as
#     the original shape of the distribution is flat. Therefore
#     one can simply use different tsallist fits as weith function for
#     for flat p_T distribution


# TODO: Rewrite this as a pipeline
def corrected_spectrum(directory, join_point=7):
        genhist = 'hPt_#pi^{0}_primary_'
        particle = "#pi^{0}"

        # Define inputs and options for different productions
        dinp, dopt = Input(DataVault().file("data"), 'Phys', label='data'), Options()

        # SPMC
        unified_inputs = {
            DataVault().file("single #pi^{0}", "low"): (0, join_point),
            DataVault().file("single #pi^{0}", "high"): (join_point, 20)
        }

        estimator = EfficiencyMultirange(
           MultirangeEfficiencyOptions.spmc(unified_inputs, particle)
        )

        loggs = AnalysisOutput("composite_efficiency_spmc_for_corrected_yield{}".format(particle), particle)

        efficiency = estimator.transform(
           [Input(filename, "PhysEffPlain") for filename in unified_inputs],
           loggs
        )
        # loggs.plot(False)
        return CorrectedYield(dinp, dopt, efficiency)


def fit_function(rrange=(0, 7)):
    tsallis = ROOT.TF1("f", "x[0] * (x[0] )*[0]/2./3.1415*([2]-1.)*([2]-2.)/([2]*[1]*([2]*[1]+[4]*([2]-2.))) * (1.+(sqrt((x[0])*(x[0])+[3]*[3])-[4])/([2]*[1])) ** (-[2])", *rrange);

    # No Weights
    # tsallis.SetParameters(2.4, 0.139, 6.880);

    # Weights0
    # tsallis.SetParameters(0.014948507575731244, 0.2874438247098432, 9.895472915554668)

    # Weights1
    tsallis.SetParameters(0.014960701090585591, 0.287830380417601, 9.921003040859755)
                         # [0.014850211992453644, 0.28695967166609104, 9.90060126848571

    tsallis.FixParameter(3, 0.135);
    tsallis.FixParameter(4, 0.135);
    tsallis.SetLineColor(46)
    return tsallis


class WeighSingleParticleMC(unittest.TestCase):

    def setUp(self):
        self.stop = 'discover' not in sys.argv


    def test_calculate_weights_parameters(self):
        cspectrum = corrected_spectrum('nonlin', 6)
        fitf = fit_function()
        cyield = cspectrum.evaluate()
        cyield.Fit(fitf, "MR")
        drawf = fit_function((0, 100))
        cyield.Draw()
        drawf.Draw("same")

        parameters = map(fitf.GetParameter, range(fitf.GetNpar()))
        print parameters, fitf.GetChisquare() / fitf.GetNDF()

        ROOT.gROOT.SetBatch(False)
        diff = cmpr.Comparator()
        diff.compare(cyield)


    @unittest.skip('')
    def test_different_iterations(self):
        w0 = self.corrected_spectrum('nonlin0').evaluate()
        w0.label = 'w0'

        w1 = self.corrected_spectrum('nonlin1').evaluate()
        w1.label = 'w1'

        diff = cmpr.Comparator()
        w1w0 = diff.compare(w1, w0)

