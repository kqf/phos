import unittest
import ROOT

from spectrum.comparator import Comparator
from tools.feeddown import FeeddownEstimator
from vault.datavault import DataVault




class FedddownTest(unittest.TestCase):

    def setUp(self):
        self.infile = DataVault().file("pythia8")
        # self.infile = 'scaled-LHC17f8a'
        self.selection = 'MCStudyOnlyTender'
        self.particles = '', 'K^{s}_{0}'#, '#Lambda', '#pi^{+}', '#pi^{-}'



    def test_feeddown_correction(self):
        func = self.fit_function()
        estimator = FeeddownEstimator(self.infile, self.selection, func)
        feeddown_ratio, feeddown_errors = estimator.estimate('K^{s}_{0}')
        feeddown_ratio.logy = False

        diff = Comparator(crange = (0, 0.04), rrange = (-1, -1))#, oname = '{0}_spectrum_{1}'.format(self.infile, ptype))

        feeddown_errors.SetTitle('feeddown correction approximation')
        feeddown_errors.label = 'approx'
        feeddown_errors.SetOption('e3')
        diff.compare(feeddown_ratio, feeddown_errors)        


    # Just compare all contributions, don't use it for error estimation
    # 
    @unittest.skip('')
    def test_feeddown_for_different_particles(self):
        func = self.fit_function()
        estimator = FeeddownEstimator(self.infile, self.selection, func)

        # Feeddown correction from different particles
        particles = map(estimator.estimate, self.particles)
        for pp in particles:
            for p in pp:
                p.logy = False

        diff = Comparator(crange = (0, 0.1))#, oname = '{0}_spectrum_{1}'.format(self.infile, ptype))
        diff.compare(particles)

    @staticmethod
    def fit_function():
        func_feeddown = ROOT.TF1("func_feeddown", "[2] * (1.+[0]*TMath::Exp(-x/2*x/2/2./[1]/[1]))", 0, 100);
        func_feeddown.SetParNames('A', '#sigma', 'E_{scale}')
        func_feeddown.SetParameter(0, -1.4)
        func_feeddown.SetParameter(1, 0.33)
        func_feeddown.SetParLimits(1, 0, 10)
        func_feeddown.FixParameter(2, 0.02)
        return func_feeddown
