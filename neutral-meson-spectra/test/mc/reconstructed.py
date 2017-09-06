
import ROOT
import os.path
import unittest

from spectrum.spectrum import Spectrum
from spectrum.input import NoMixingInput, read_histogram
from spectrum.sutils import get_canvas, adjust_canvas
from spectrum.options import Options
from spectrum.sutils import wait
from spectrum.comparator import Visualizer, Comparator
from spectrum.sutils import save_tobject, scalew

from spectrum.broot import BROOT as br


class Estimator(object):

    def __init__(self):
        super(Estimator, self).__init__()

    def estimate(self, ptype = 'secondary'):
        inp = lambda x: NoMixingInput(self.infile, self.selection, '{0}_{1}_{2}'.format(self.hname, ptype, x))
        f = lambda x: Spectrum(inp(x), Options.fixed_peak(x)).evaluate().spectrum

        particles = map(f, self.particles_set[ptype])
        map(scalew, particles)

        generated = self.get_baseline()

        # diff = Comparator(crange = (1e-15, 1.))
        diff = Comparator((1, 1), oname = '{0}_spectrum_{1}'.format(self.infile, ptype))
        diff.compare(particles)
        diff.compare_ratios(particles, generated, logy = True)

        total, summed = particles[0], br.sum(particles[1:], 'summed')
        diff.compare(total, summed)


    def get_baseline(self):
        generated = read_histogram(self.infile, self.selection, 'hPt_#pi^{0}', 'generated')
        scalew(generated)
        return generated 


class ParticleContributions(unittest.TestCase, Estimator):

    def setUp(self):
        self.infile = 'Pythia-LHC16-a5'
        # self.infile = 'scaled-LHC17f8a'
        self.selection = 'MCStudyOnlyTender'
        self.hname = 'MassPt_#pi^{0}'
        self.particles_set = {
            'primary':   ['', '#rho^{+}', '#rho^{-}', 'K^{s}_{0}', '#Lambda', '#pi^{+}', '#pi^{-}', '#eta', '#omega', 'K^{*+}', 'K^{*-}', 'K^{*0}', '#barK^{*0}', 'K^{+}', 'K^{-}', '#Sigma^{0}'],
            'secondary': ['', 'K^{s}_{0}', '#Lambda', '#pi^{+}', '#pi^{-}', '#eta', '#omega'],
            'feeddown':  ['', 'K^{s}_{0}', '#Lambda', '#pi^{+}', '#pi^{-}', '#eta', '#omega']
        }


    def testContributions(self):
        # self.estimate('primary')
    	self.estimate('secondary')
        # self.estimate('feeddown')
