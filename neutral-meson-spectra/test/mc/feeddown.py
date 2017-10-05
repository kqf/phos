
from spectrum.spectrum import Spectrum
from spectrum.input import NoMixingInput, read_histogram
from spectrum.options import Options
from spectrum.sutils import wait
from spectrum.comparator import Comparator

from spectrum.broot import BROOT as br

import ROOT

import os.path
import unittest


class FeeddownEstimator(object):

    def __init__(self, infile, selection):
        super(FeeddownEstimator, self).__init__()
        self.infile = infile
        self.selection = selection
        self.hname = 'MassPt_#pi^{0}_feeddown_'
        self.label = 'feeddown'
        self.baseline = self._baseline()

    def spectrum(self, histname, x):
        inp = NoMixingInput(self.infile, self.selection, histname)
        # CWR: Check if this is the final parametrization
        spectrum = Spectrum(inp, Options.fixed_peak(x if x else 'all')).evaluate().spectrum
        return br.scalew(spectrum) 

    def estimate(self, ptype = ''):
        feeddown = self.spectrum(self.hname + ptype, ptype)
        feeddown.fitfunc = self.fit_function()

        diff = Comparator((1, 1))
        result = diff.compare(feeddown, self.baseline)
        result.label = ptype if ptype else 'all secondary'
        return result

    def _baseline(self):
        # generated = read_histogram(self.infile, self.selection, 'hPt_#pi^{0}', 'generated')
        # br.scalew(generated)
        # Estimate this quantity in a following way
        base = self.spectrum('MassPt', '\pi^{0}_{rec} all')
        base.priority = -1
        return base

    @staticmethod
    def fit_function():
        func_feeddown = ROOT.TF1("func_feeddown", "[2] * (1.+[0]*TMath::Exp(-x/2*x/2/2./[1]/[1]))", 0, 100);
        func_feeddown.SetParNames('A', '#sigma', 'E_{scale}')
        func_feeddown.SetParameter(0, -1.4)
        func_feeddown.SetParameter(1, 0.33)
        func_feeddown.SetParLimits(1, 0, 10)
        func_feeddown.FixParameter(2, 0.02)
        return func_feeddown

  

class FedddownTest(unittest.TestCase):

    def setUp(self):
        self.infile = 'Pythia-LHC16-a5'
        # self.infile = 'scaled-LHC17f8a'
        self.selection = 'MCStudyOnlyTender'
        self.particles = '', 'K^{s}_{0}'#, '#Lambda', '#pi^{+}', '#pi^{-}'



    def test_feeddown_correction(self):
        estimator = FeeddownEstimator(self.infile, self.selection)
        feeddown_ratio = estimator.estimate('K^{s}_{0}')

        diff = Comparator(crange = (0, 0.1))#, oname = '{0}_spectrum_{1}'.format(self.infile, ptype))
        diff.compare(feeddown_ratio)        


    # TODO: calculate error range parameters for feeddown correction
    #
    def testExtractParameters(self):
        pass

    # Just compare all contributions, don't use it for error estimation
    # 
    @unittest.skip('')
    def test_feeddown_for_different_particles(self):
        estimator = FeeddownEstimator(self.infile, self.selection)

        # Feeddown correction from different particles
        particles = map(estimator.estimate, self.particles)
        for p in particles:
            p.logy = False

        diff = Comparator(crange = (0, 0.1))#, oname = '{0}_spectrum_{1}'.format(self.infile, ptype))
        diff.compare(particles)