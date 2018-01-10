import unittest

from spectrum.spectrum import CompositeSpectrum
from spectrum.input import Input
from spectrum.options import Options
from spectrum.broot import BROOT as br
from spectrum.comparator import Comparator
import spectrum.comparator as cmpr
import spectrum.sutils as su



# Check 
class TestPi0EtaMassRatio(unittest.TestCase):

    def test_mass_ratio(self):
        inputs_pi0 = {
            Input('/single/nonlin0/LHC17j3b1', 'PhysEffOnlyTender'): (0, 5.5), 
            Input('/single/nonlin0/LHC17j3b2', 'PhysEffOnlyTender'): (5.5, 20)
        }

        pi0 = CompositeSpectrum(inputs_pi0, Options('pi0'))

        inputs_eta = {
            Input('/single/nonlin1/LHC17j3c1', 'PhysEffOnlyTender'): (0, 10), 
            Input('/single/nonlin1/LHC17j3c2', 'PhysEffOnlyTender'): (10, 20)
        }

        options_eta = Options('eta', particle='eta')


        eta = CompositeSpectrum(inputs_eta, options_eta)

        diff = Comparator()

        diff.compare(
            pi0.evaluate().mass, 
            eta.evaluate().mass
        )

