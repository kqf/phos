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
        sinput = Input('LHC16-old', 'TOFStudyTender', 'MassEnergy%s_SM0')
        self.eff_calculator = TagAndProbe(sinput, 3)

        sinput = Input('LHC16-old', 'TOFStudyTender', 'MassEnergy%s_SM0')
        self.eff_calculator_improved = TagAndProbe(sinput, 3)


    @staticmethod
    def efficincy_function():
        func_nonlin = ROOT.TF1("tof_eff", "[2] * (1.+[0]*TMath::Exp(-x/2*x/2/2./[1]/[1]) - pol3(3) * (x > 6))", 0, 100);
        func_nonlin.SetParNames('A', '#sigma', 'E_{scale}')
        func_nonlin.SetParameter(0, -0.05)
        func_nonlin.SetParameter(1, 0.6)
        func_nonlin.SetParLimits(1, 0, 10)
        func_nonlin.SetParameter(2, 1.04)
        return func_nonlin


    def test_estimate_tof_efficiency(self):
        fitf = self.efficincy_function()
        eff = self.eff_calculator.eff(True, fitf)


    def testCompareEfficienciesDifferentMethods(self):
        eff1 = self.eff_calculator.eff()
        eff2 = self.eff_calculator_improved.eff()

        diff = Comparator()
        diff.compare(eff1, eff2)


    @unittest.skip('Debug')
    def test_different_modules(self):
        conf = 'config/test_tagandprobe_modules.json'
        estimators = [TagAndProbe(self.infile, self.sel, 'MassEnergy%s' + '_SM%d' % i, cut='TOF', full='All', conffile=conf) for i in range(1, 5)]
        f = lambda i, x, y: br.ratio(x, y, 'TOF efficiency in different modules; E, GeV', 'SM%d' % i)
        multiple = [[f(i + 1, *(e.estimate()))] for i, e in enumerate(estimators)]

        c1 = adjust_canvas(gcanvas())
        diff = Comparator()
        diff.compare(multiple)



if __name__ == '__main__':
    main()