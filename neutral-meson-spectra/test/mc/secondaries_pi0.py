
from spectrum.spectrum import Spectrum
from spectrum.input import Input, TimecutInput
from spectrum.sutils import get_canvas, adjust_canvas
from spectrum.options import Options
from spectrum.sutils import wait
from spectrum.comparator import Visualizer, Comparator
from spectrum.sutils import save_tobject

import ROOT

import os.path
import unittest


class SecondaryContributions(unittest.TestCase):

    def testSecondaries(self):
        f = lambda x, y, z: Spectrum(x, label=y, mode = 'q', options = z).evaluate()

        histname = 'MassPtN3_primary_#rho^{+}'
        self.rho = f(Input('input-data/Pythia-LHC16-a2.root', 'MCStudyOnlyTender', histname).read(), '#rho^{+}', Options())
        self.rho[2].Draw()
        wait()

        # diff = Comparator()
        # diff.compare(self.rho)

