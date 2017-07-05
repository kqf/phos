from test.mc.constributions_of_secondaries_to_pi0_spectrum import Estimator

import ROOT

import os.path
import unittest


class FeedDownCorrection(unittest.TestCase, Estimator):

    def setUp(self):
        self.infile = 'input-data/Pythia-LHC16-a2.root'
        self.selection = 'MCStudyOnlyTender'
        self.hname = 'MassPtN3'
        # TODO: Select necessary particles
        self.particle_names = ['', '#pi^{-}', '#pi^{+}', '#eta', '#omega', 'K^{s}_{0}', '#Lambda', '#rho^{-}', '#rho^{+}']


    def testContributions(self):
    	self.estimate('primary')
