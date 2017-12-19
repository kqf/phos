import unittest
import sys

import ROOT
from spectrum.sutils import gcanvas, wait, adjust_canvas
from spectrum.input import Input
from spectrum.invariantmass import InvariantMass
from spectrum.comparator import Comparator
from spectrum.spectrum import Spectrum
from spectrum.options import Options
from spectrum.outputcreator import OutputCreator

from spectrum.broot import BROOT as br

from tools.probe import TagAndProbe
import numpy as np
import array as arr

ROOT.TH1.AddDirectory(False)


class TagAndProbeEfficiencyTOF(unittest.TestCase):

    def setUp(self):
        self.canvas = gcanvas()

    @staticmethod
    def efficincy_function():
        tof_eff = ROOT.TF1("tof_eff", 
            # "[2] * (1.+[0]*TMath::Exp(-TMath::Power(x/[1], 2.) / 2.)) "
            "1 - [2] / (1 + TMath::Exp(x * [0] + [1]))"
            " - [3] * TMath::Exp(x * [4])"
            , 0, 20)

        tof_eff.SetParNames('A', '#sigma', 'Eff_{scale}')
        tof_eff.SetParameter(0, -1.30534e+00)
        tof_eff.SetParameter(1, 1.02604e+01)
        tof_eff.SetParameter(2, 5.70061e-01)
        tof_eff.SetParameter(3, 1.06068e+00)
        tof_eff.SetParameter(4, -1.62810e+00)

        return tof_eff 


    def fit_tof_efficiency(self, dataset):
        sinput = Input(dataset, 'TagAndProbleTOFOnlyTender', 'MassEnergy%s_SM0')
        probe_estimator = TagAndProbe(sinput)
        fitf = self.efficincy_function()

        eff = probe_estimator.eff(True, fitf)
        eff.Fit(fitf, 'R')
        diff = Comparator(crange = (0.2, 1.05))
        diff.compare(eff)
        return eff


    @unittest.skip('Debug')
    def test_estimate_tof_efficiency(self):
        fit_tof_efficiency('/new-calibration/LHC16')


    @unittest.skip('Debug')
    def test_different_modules(self):
        conf = 'config/test_tagandprobe_modules.json'

        inputs = [Input('/uncorrected/LHC16', 'TagAndProbleTOFOnlyTender', 'MassEnergy%s' + '_SM{0}'.format(i)) for i in range(1, 5)] 
        estimators = [TagAndProbe(si).eff(False) for si in inputs]
        for i, e in enumerate(estimators):
            e.SetTitle('TOF efficiency in different modules; E, GeV; TOF efficiency')
            e.label = 'SM{0}'.format(i + 1)
            e.logy = 0

        canvas = adjust_canvas(gcanvas())
        diff = Comparator(crange = (0, 1))
        diff.compare(estimators)


    # Test new and old tof calibrations 
    def test_efficiencies_different(self):
        paths = {
            '/new-calibration/LHC16': '2017',
            '/uncorrected/LHC16': '2016'
            }
        efficiencies = map(self.fit_tof_efficiency, paths.keys())
        for e, l in zip(efficiencies, paths.values()):
            e.label = l

        diff = Comparator(rrange = (0.2, 1.01))
        diff.compare(efficiencies)


if __name__ == '__main__':
    main()