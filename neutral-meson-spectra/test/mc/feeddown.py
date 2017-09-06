
from spectrum.spectrum import Spectrum
from spectrum.input import NoMixingInput, read_histogram
from spectrum.sutils import get_canvas, adjust_canvas
from spectrum.options import Options
from spectrum.sutils import wait
from spectrum.comparator import Visualizer, Comparator
from spectrum.sutils import save_tobject, scalew

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
        self.baseline = self.get_baseline()

    def spectrum(self, histname, x):
        # TODO: Check if this is the final parametrization
        inp = NoMixingInput(self.infile, self.selection, histname)
        spectrum = Spectrum(inp, Options.fixed_peak(x if x else 'all')).evaluate().spectrum
        return scalew(spectrum) 

    def estimate(self, ptype = ''):
        feeddown = self.spectrum(self.hname + ptype, ptype)
        # What name should I use here?
        diff = Comparator((1, 1))#, oname = '{0}_spectrum_{1}'.format(self.infile, ptype))
        result = diff.compare(feeddown, self.baseline)
        result.label = ptype if ptype else 'all secondary'
        return result


    def get_baseline(self):
        # generated = read_histogram(self.infile, self.selection, 'hPt_#pi^{0}', 'generated')
        # scalew(generated)
        # Estimate this quantity in a following way
        return self.spectrum('MassPt', '\pi^{0}_{rec} all')


class FedddownTest(unittest.TestCase):

    def setUp(self):
        self.infile = 'Pythia-LHC16-a5'
        # self.infile = 'scaled-LHC17f8a'
        self.selection = 'MCStudyOnlyTender'
        self.particles = '', 'K^{s}_{0}', '#Lambda', '#pi^{+}', '#pi^{-}'


    def getFitFunction(self):
        pass

    def testFeeddownFromDifferentParticles(self):
        estimator = FeeddownEstimator(self.infile, self.selection)

        # Feeddown correction from different particles
        particles = map(estimator.estimate, self.particles)
        for p in particles:
            p.logy = False

        diff = Comparator(crange = (0, 0.1))#, oname = '{0}_spectrum_{1}'.format(self.infile, ptype))
        return diff.compare(particles)

    def testCompareProductions(self):
        pass

        
    # Extract parameters of feeddown correction
    #
    def testExtractParameters(self):
        pass

