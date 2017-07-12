from test.mc.constributions_of_secondaries_to_pi0_spectrum import Estimator
from spectrum.input import read_histogram
from spectrum.ptanalyzer import PtDependent
from spectrum.comparator import Comparator

import ROOT

import os.path
import unittest


class InspectSources(unittest.TestCase):

    def setUp(self):
        self.infile = 'input-data/Pythia-LHC16-a4.root'
        self.selection = 'MCStudyOnlyTender'
        self.particle_names = ['', '#pi^{-}', '#pi^{+}', '#eta', '#omega', 'K^{s}_{0}', '#Lambda', '#rho^{-}', '#rho^{+}']

    def inspect(self, ptype):
        particles = [read_histogram(self.infile, self.selection, 'hPt_#pi^{0}_%s_%s' % (ptype, p), p) for p in self.particle_names] 
        map(PtDependent.divide_bin_width, particles)

        for p in particles:
        	p.logy = True

        diff = Comparator()
        diff.compare(particles)


    def testContributions(self):
    	self.inspect('secondary')
    	self.inspect('primary')
    	self.inspect('feeddown')
