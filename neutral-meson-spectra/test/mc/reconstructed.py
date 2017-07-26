
from spectrum.spectrum import Spectrum
from spectrum.input import Input, TimecutInput, read_histogram
from spectrum.sutils import get_canvas, adjust_canvas
from spectrum.options import Options
from spectrum.sutils import wait
from spectrum.comparator import Visualizer, Comparator
from spectrum.sutils import save_tobject, scalew

import ROOT

import os.path
import unittest

from spectrum.sutils import hsum


# TODO: Correct names in the output
class Estimator(object):

    def __init__(self):
        super(Estimator, self).__init__()

    def estimate(self, ptype = 'secondary'):
        options = Options()
        options.fit_mass_width = False

        inp = lambda x: Input(self.infile, self.selection, '{0}_{1}_{2}'.format(self.hname, ptype, x))
        f = lambda x: Spectrum(inp(x), label= x if x else 'all', mode = 'd', options = options).evaluate()[2]

        particles = map(f, self.particle_names)
        map(scalew, particles)

        generated = self.get_baseline()

        # diff = Comparator(crange = (1e-15, 1.))
        diff = Comparator((1, 1))
        diff.compare(particles)
        diff.compare_ratios(particles, generated, logy = True)

        total, summed = particles[0], hsum(particles[1:], 'summed')
        diff.compare(total, summed)


    def get_baseline(self):
        generated = read_histogram(self.infile, self.selection, 'hPt_#pi^{0}', 'generated')
        scalew(generated)
        return generated 


class ParticleContributions(unittest.TestCase, Estimator):

    def setUp(self):
        self.infile = 'input-data/Pythia-LHC16-a5.root'
        # self.infile = 'input-data/scaled-LHC17f8a.root'
        self.selection = 'MCStudyOnlyTender'
        self.hname = 'MassPt_#pi^{0}'
        # self.particle_names = ['', '#pi^{-}', '#pi^{+}', '#eta', '#omega', 'K^{s}_{0}', '#Lambda', '#rho^{-}', '#rho^{+}', 'K^{*-}', '#barK^{*0}', 'K^{*0}', 'K^{*+}']
        self.particle_names = '', 'K^{s}_{0}', '#pi^{-}', '#pi^{+}', '#Lambda'


    def testContributions(self):
        # self.estimate('primary')
    	# self.estimate('secondary')
        self.estimate('feeddown')
