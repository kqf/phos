import unittest

import ROOT
from spectrum.input import Input
from spectrum.options import Options

from tools.probe import TagAndProbe
from vault.datavault import DataVault


class TestProbe(unittest.TestCase):

    def test_interface(self):
        probe = TagAndProbe(
            DataVault().file("data")
        )
        probe.eff()

