from spectrum.spectrum import Spectrum
from spectrum.input import Input, TimecutInput, read_histogram
from spectrum.sutils import get_canvas, adjust_canvas
from spectrum.options import Options
from spectrum.comparator import Visualizer, Comparator
from spectrum.sutils import save_tobject, scalew

import ROOT

import os.path
import unittest


class RawYieldSystematicError(unittest.TestCase):

    def setUp(self):
        # This should be studied on corrected yield
        #
        self.infile = 'LHC16'
        self.selection = 'PhysOnlyTender'


    def testRawYieldSysError(self):
        spectrums, options = [], Options('', mode = 'd')
        for par in ['CrystalBall', 'Gaus']:
            for nsigmas in [2, 3]:
                options.pt.label = 'n#sigma = {0} {1}'.format(nsigmas, par)
                options.spectrum.nsigmas = nsigmas
                options.param.fitf = par
                
                spectrum = self.spectrum(options)
                spectrums.append(spectrum)

        diff = Comparator()
        diff.compare(spectrums)


    def spectrum(self, options):
        inp = Input(self.infile, self.selection)
        spectrum = Spectrum(inp, options).evaluate().spectrum
        return scalew(spectrum)  





