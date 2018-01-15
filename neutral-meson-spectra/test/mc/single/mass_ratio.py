import unittest

from spectrum.spectrum import CompositeSpectrum
from spectrum.input import Input
from spectrum.options import Options
from spectrum.broot import BROOT as br
from spectrum.outputcreator import RangeTransformer
from spectrum.comparator import Comparator
import spectrum.comparator as cmpr
import spectrum.sutils as su



# Check 
class TestPi0EtaMassRatio(unittest.TestCase):

    def test_mass_ratio(self):
        compare_range = 0.8, 14
        inputs_pi0 = {
            Input('/single/nonlin/LHC17j3b1', 'PhysEffOnlyTender', label='#pi^{0}'): (0, 5.5), 
            Input('/single/nonlin/LHC17j3b2', 'PhysEffOnlyTender', label='#pi^{0}'): (5.5, 20)
        }

        diff = Comparator()

        pi0 = CompositeSpectrum(inputs_pi0, Options.spmc((0, 5.5), 'pi0'))
        pi0_mass = pi0.evaluate().mass
        pi0_massf = pi0.RangeTransformer(Options(), '#pi^{0}').fit_mass(pi0_mass)
        diff.compare(pi0_mass)

        pi0_massf.SetRange(*compare_range)
        pi0_massf.Draw()
        su.wait()


        inputs_eta = {
            Input('/single/nonlin1/LHC17j3c1', 'PhysEffOnlyTender', label='#eta'): (0, 10), 
            Input('/single/nonlin1/LHC17j3c2', 'PhysEffOnlyTender', label='#eta'): (10, 20)
        }

        options_eta = Options.spmc((0, 10), particle='eta')

        eta = CompositeSpectrum(inputs_eta, options_eta)
        eta_mass = eta.evaluate().mass
        eta_massf = eta.RangeTransformer(Options(), "#eta").fit_mass(eta_mass)
        eta_massf.SetRange(*compare_range)
        diff.compare(eta_mass)

        eta_mass_approx = eta_massf.GetHistogram()
        eta_mass_approx.SetTitle("Fitted masses of neutral mesons")
        eta_mass_approx.label = 'm_{#eta}'
        pi0_mass_approx = pi0_massf.GetHistogram()
        pi0_mass_approx.label = 'm_{#pi^{0}}'

        diff = Comparator(crange=(0.1, 0.7))
        diff.compare(
            eta_mass,
            pi0_mass
        )

