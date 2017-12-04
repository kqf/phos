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

from tools.probe import TagAndProbe, TagAndProbe
import numpy as np
import array as arr

ROOT.TH1.AddDirectory(False)


class TagAndProbeEfficiencyTOF(unittest.TestCase):

    def setUp(self):
        self.canvas = gcanvas()

    @staticmethod
    def efficincy_function():
        func_nonlin = ROOT.TF1("tof_eff", "[2] * (1.+[0]*TMath::Exp(-x/2*x/2/2./[1]/[1]) - pol3(3) * (x > 6))", 0, 100);
        func_nonlin.SetParNames('A', '#sigma', 'E_{scale}')
        func_nonlin.SetParameter(0, -0.05)
        func_nonlin.SetParameter(1, 0.6)
        func_nonlin.SetParLimits(1, 0, 10)
        func_nonlin.SetParameter(2, 1.04)
        return func_nonlin


    # @unittest.skip('Debug')
    def test_estimate_tof_efficiency(self):
        sinput = Input('/uncorrected/LHC16', 'TagAndProbleTOFOnlyTender', 'MassEnergy%s_SM0')
        probe_estimator = TagAndProbe(sinput)
        fitf = self.efficincy_function()
        eff = probe_estimator.eff(True, fitf)


    @unittest.skip('Debug')
    def test_compare_different_methods(self):
        sinput = Input('/uncorrected/LHC16', 'TagAndProbleTOFOnlyTender', 'MassEnergy%s_SM0')
        eff1 = TagAndProbe(sinput).eff()

        # Improved version
        sinput = Input('/uncorrected/LHC16', 'TagAndProbleTOFOnlyTender', 'MassEnergy%s_SM0')
        eff2 = TagAndProbe(sinput).eff()

        diff = Comparator()
        diff.compare(eff1, eff2)


    @unittest.skip('Debug')
    def test_different_modules(self):
        conf = 'config/test_tagandprobe_modules.json'

        inputs = [Input('/uncorrected/LHC16', 'TagAndProbleTOFOnlyTender', 'MassEnergy%s' + '_SM{0}'.format(i)) for i in range(1, 5)] 
        estimators = [TagAndProbe(si, 3).eff() for si in inputs]
        for i, e in enumerate(estimators):
            e.SetTitle('TOF efficiency in different modules; E, GeV; TOF efficiency')
            e.label = 'SM{0}'.format(i + 1)
            e.logy = 0

        canvas = adjust_canvas(gcanvas())
        diff = Comparator(crange = (0, 1))
        diff.compare(estimators)



if __name__ == '__main__':
    main()