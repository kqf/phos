
from spectrum.spectrum import Spectrum
from spectrum.input import Input, TimecutInput, read_histogram
from spectrum.sutils import get_canvas, adjust_canvas
from spectrum.options import Options
from spectrum.sutils import wait
from spectrum.comparator import Visualizer, Comparator
from spectrum.sutils import save_tobject
from spectrum.ptanalyzer import PtDependent

import ROOT

import os.path
import unittest


class SecondaryContributions(unittest.TestCase):

    def setUp(self):
        self.infile = 'input-data/Pythia-LHC16-a2.root'
        self.selection = 'MCStudyOnlyTender'
        self.hname = 'MassPtN3'
        # TODO: Add common histogram for all the particles
        self.particle_names = ['#pi^{-}', '#pi^{+}', '#eta', '#omega', 'K^{s}_{0}', '#Lambda', '#rho^{-}', '#rho^{+}']



    def estimate(self, ptype = 'primary'):
        options = Options()
        options.fit_mass_width = False
        f = lambda x, y: Spectrum(x, label=y, mode = 'q', options = options).evaluate()
        histstam = '{0}_{1}_'.format(self.hname, ptype)
        particles = [f(Input(self.infile, self.selection, histstam + pnames).read(), pnames)[2] for pnames in self.particle_names]
        map(PtDependent.divide_bin_width, particles)

        generated = read_histogram(self.infile, self.selection, 'hPtGeneratedMC_#pi^{0}', 'generated')
        PtDependent.divide_bin_width(generated)

        diff = Comparator()
        diff.compare_ratios(particles, generated)



    def testSecondaries(self):
    	self.estimate('primary')
    	self.estimate('secondary')




