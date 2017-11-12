import unittest

import ROOT
from spectrum.input import Input
from spectrum.options import Options

from tools.probe import TagAndProbe


class TestProbe(unittest.TestCase):

    def test_interface(self):
        sinput = Input('LHC16-old', 'TOFStudyTender', 'MassEnergy%s_SM0')
        nsigma = 3

        probe = TagAndProbe(sinput, nsigma)
        probe.eff()

