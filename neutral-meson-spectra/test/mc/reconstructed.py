
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

from spectrum.sutils import hsum


class Estimator(object):

    def __init__(self):
        super(Estimator, self).__init__()

    def estimate(self, ptype = 'secondary'):
        options = Options()
        options.fit_mass_width = False

        histstame = '{0}_{1}_'.format(self.hname, ptype)
        f = lambda x: Spectrum(Input(self.infile, self.selection, histstame + x).read(), label=x, mode = 'q', options = options).evaluate()[2]

        particles = map(f, self.particle_names)
        map(PtDependent.divide_bin_width, particles)

        generated = self.get_baseline()

        # diff = Comparator(crange = (1e-15, 1.))
        diff = Comparator()
        diff.compare(particles)
        diff.compare_ratios(particles, generated, logy = True)

        total, summed = particles[0], hsum(particles[1:], 'summed')
        diff.compare(total, summed)


    def get_baseline(self):
        generated = read_histogram(self.infile, self.selection, 'hPt_#pi^{0}', 'generated')
        PtDependent.divide_bin_width(generated)
        return generated 


class ParticleContributions(unittest.TestCase, Estimator):

    def setUp(self):
        self.infile = 'input-data/Pythia-LHC16-a5.root'
        # self.infile = 'input-data/scaled-LHC17f8a.root'
        self.selection = 'MCStudyOnlyTender'
        self.hname = 'MassPt_#pi^{0}'
        self.particle_names = ['', '#pi^{-}', '#pi^{+}', '#eta', '#omega', 'K^{s}_{0}', '#Lambda', '#rho^{-}', '#rho^{+}', 'K^{*-}', '#barK^{*0}', 'K^{*0}', 'K^{*+}']


    def testContributions(self):
        # self.estimate('primary')
    	# self.estimate('secondary')
        self.estimate('feeddown')
