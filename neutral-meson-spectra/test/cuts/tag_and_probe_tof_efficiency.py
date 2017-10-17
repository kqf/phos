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

from spectrum.probe import ProbeSpectrum, TagAndProbe, TagAndProbeRigorous
import numpy as np
import array as arr

ROOT.TH1.AddDirectory(False)


class TagAndProbeEfficiencyTOF(unittest.TestCase):

    def setUp(self):
        self.canvas = gcanvas()
        self.infile = 'input-data/LHC16-old.root'
        self.sel = 'TOFStudyTender'
        self.eff_calculator_relaxed = TagAndProbe(self.infile, self.sel, 'MassEnergy%s_SM0', cut='TOF', full='All')
        self.eff_calculator = TagAndProbeRigorous(self.infile, self.sel, 'MassEnergy%s_SM0', cut='TOF', full='All')

    @staticmethod
    def get_efficincy_function():
        func_nonlin = ROOT.TF1("tof_eff", "[2] * (1.+[0]*TMath::Exp(-x/2*x/2/2./[1]/[1]) - pol3(3) * (x > 6))", 0, 100);
        func_nonlin.SetParNames('A', '#sigma', 'E_{scale}')
        func_nonlin.SetParameter(0, -0.05)
        func_nonlin.SetParameter(1, 0.6)
        func_nonlin.SetParLimits(1, 0, 10)
        func_nonlin.SetParameter(2, 1.04)
        return func_nonlin

    # @unittest.skip('Debug')
    def testEstimateEfficiency(self):
        results = self.eff_calculator.estimate()

        # Decorate
        f = lambda x: x.SetTitle('Energy spectrum of probe photons; E_{#gamma}, GeV')
        map(f, results)

        fitfunc = self.get_efficincy_function()
        for r in results:
            r.fitfunc = fitfunc

        diff = Comparator()
        diff.compare(results)

    @unittest.skip('Debug')
    def testCompareEfficienciesDifferentMethods(self):
        cut, full = self.eff_calculator.estimate()
        eff1 = br.ratio(cut, full, 'TOF efficiency; E, GeV', 'rigorous')

        cut, full = self.eff_calculator_relaxed.estimate()
        eff2 = br.ratio(cut, full, 'TOF efficiency; E, GeV', 'simple')
        
        diff = Comparator()
        diff.compare(eff1, eff2)

    @unittest.skip('Debug')
    def testDifferentModules(self):
        conf = 'config/test_tagandprobe_modules.json'
        estimators = [TagAndProbeRigorous(self.infile, self.sel, 'MassEnergy%s' + '_SM%d' % i, cut='TOF', full='All', conffile=conf) for i in range(1, 5)]
        f = lambda i, x, y: br.ratio(x, y, 'TOF efficiency in different modules; E, GeV', 'SM%d' % i)
        multiple = [[f(i + 1, *(e.estimate()))] for i, e in enumerate(estimators)]

        c1 = adjust_canvas(gcanvas())
        diff = Comparator()
        diff.compare(multiple)



if __name__ == '__main__':
    main()