from spectrum.input import read_histogram
from spectrum.ptanalyzer import PtDependent
from spectrum.comparator import Comparator

import ROOT
import os.path
import unittest

from spectrum.sutils import hsum, scalew

class InspectSources(unittest.TestCase):

    def setUp(self):
        self.infile = 'input-data/Pythia-LHC16-a5.root'
        # self.infile = 'input-data/scaled-LHC17f8a.root'
        self.selection = 'MCStudyOnlyTender'
        self.particle_names = ['', '#pi^{-}', '#pi^{+}', '#eta', '#omega', 'K^{s}_{0}', '#Lambda', '#rho^{-}', '#rho^{+}', 'K^{*-}', '#barK^{*0}', 'K^{*0}', 'K^{*+}']


    def get_baseline(self):
        # TODO: Replace this histogram with hPt_#pi^{0}
        generated = read_histogram(self.infile, self.selection, 'hPt_#pi^{0}', 'generated', norm = True)
        scalew(generated)
        return generated 


    def inspect(self, ptype):
        particles = [read_histogram(self.infile, self.selection, 'hPt_#pi^{0}_%s_%s' % (ptype, p), p, norm = True) for p in self.particle_names] 
        map(scalew, particles)

        for p in particles:
        	p.logy = True

        generated = self.get_baseline()

        diff = Comparator(crange = (1e-15, 1.))
        diff.compare(particles)
        diff.compare_ratios(particles, generated, logy= True)

        total, summed = particles[0], hsum(particles[1:], 'summed')
        diff.compare(total, summed)

  
    def testContributions(self):
    	self.inspect('secondary')
    	self.inspect('primary')
    	self.inspect('feeddown')
