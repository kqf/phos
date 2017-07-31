from spectrum.input import read_histogram
from spectrum.ptanalyzer import PtDependent
from spectrum.comparator import Comparator

import ROOT
import os.path
import unittest

from spectrum.sutils import hsum, scalew

class InspectSources(unittest.TestCase):

    def setUp(self):
        # self.infile = 'input-data/Pythia-LHC16-a5.root'
        self.infile = 'scaled-LHC17f8a'
        self.selection = 'MCStudyOnlyTender'
        self.particles_set = {
            'primary':   ['', '#rho^{+}', '#rho^{-}', 'K^{s}_{0}', '#Lambda', '#pi^{+}', '#pi^{-}', '#eta', '#omega', 'K^{*+}', 'K^{*-}', 'K^{*0}', '#barK^{*0}', 'K^{+}', 'K^{-}', '#Sigma^{0}'],
            'secondary': ['', 'K^{s}_{0}', '#Lambda', '#pi^{+}', '#pi^{-}', '#eta', '#omega'],
            'feeddown':  ['', 'K^{s}_{0}', '#Lambda', '#pi^{+}', '#pi^{-}', '#eta', '#omega']
        }


    def get_baseline(self):
        generated = read_histogram(self.infile, self.selection, 'hPt_#pi^{0}', 'generated', norm = True)
        scalew(generated)
        return generated 


    def inspect(self, ptype):
        f = lambda x : read_histogram(self.infile, self.selection, 'hPt_#pi^{0}_%s_%s' % (ptype, x), x if x else 'all', norm = True)
        particles = map(f, self.particles_set[ptype])
        map(scalew, particles)

        for p in particles:
        	p.logy = True

        generated = self.get_baseline()
        diff = Comparator(crange = (1e-15, 1.), oname = '{0}_spectrum_{1}'.format(ptype, self.infile))
        diff.compare(particles)

        diff = Comparator(crange = (1e-15, 1.), oname = '{0}_ratio_{1}'.format(ptype, self.infile))
        diff.compare_ratios(particles, generated, logy= True)

        diff = Comparator(crange = (1e-15, 1.), oname = '{0}_sum{1}'.format(ptype, self.infile))
        total, summed = particles[0], hsum(particles[1:], 'sum')
        diff.compare(total, summed)

  
    def testContributions(self):
    	self.inspect('secondary')
    	# self.inspect('primary')
    	# self.inspect('feeddown')
