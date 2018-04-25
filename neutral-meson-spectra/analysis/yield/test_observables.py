
import unittest
import ROOT
import sys
import json

from spectrum.options import Options
from spectrum.analysis import Analysis
from spectrum.output import AnalysisOutput
from spectrum.broot import BROOT as br


from vault.datavault import DataVault


class TestSpectrum(unittest.TestCase):

    def setUp(self):
        # Different values in some pt-bins can be explained
        # by limited statistics in those bins.
        #
        # Important:
        # This one should be set explicitely otherwise the test will fail
        # Because this global variable is set to Minuit2 in other tests
        ROOT.TVirtualFitter.SetDefaultFitter('Minuit')
        # NB: test Spectrum class, not Pt-dependent as it produces n
        # egative values due to wide integration range
        # Expected values for $\pi^0$ extraction
        with open('config/test_observables.json') as f:
            conf = json.load(f)
        self.nominal = conf[sys.platform]
        self.longMessage = True

    def validate_particle(self, particle="#pi^{0}", selection="PhysTender"):
        estimator = Analysis(
            Options(particle=particle)
        )

        output = estimator.transform(
            DataVault().input("data", "stable", selection, label='testsignal'),
            AnalysisOutput("testing_the_singnal", particle)
        )
        actual = [br.bins(h).contents for h in output]

        mymsg = '\n\nActual values:\n' + str(actual)
        for a, b, c in zip(self.nominal[particle], actual, output):
            print 'Checking ', c.GetName()
            for aa, bb in zip(a, b):
                self.assertAlmostEqual(aa, bb, msg=mymsg)

    def test_extracts_pi0_spectrum(self):
        self.validate_particle("#pi^{0}", "PhysTender")

    def test_extracts_eta_spectrum(self):
        self.validate_particle("#eta", "EtaTender")
