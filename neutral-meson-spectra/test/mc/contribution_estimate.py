
from spectrum.spectrum import Spectrum
from spectrum.input import Input
from spectrum.sutils import get_canvas, adjust_canvas
from spectrum.options import Options
from spectrum.comparator import Comparator
from spectrum.sutils import save_tobject
from spectrum.ptanalyzer import PtDependent

import ROOT

import os.path
import unittest

class Estimate(object):

    def __init__(self):
        super(Estimate, self).__init__()

    def get_hist(self, x, z, label):
        options = Options()
        options.fit_mass_width = False
        hist = Spectrum(Input(self.infile, z, x, norm = True).read(), label = label, mode = 'd', options = options).evaluate()[2]
        PtDependent.divide_bin_width(hist)
        return hist


    def estimate(self, ptype, reconstruction):
        options = Options()
        options.fit_mass_width = False
        histstame = '{0}_{1}'.format(self.hname, ptype.replace(' ', '_'))
        print histstame

        contribution = self.get_hist(histstame, self.mc_selection, ptype)
        reconstruction.priority = 0

        # diff = Comparator(crange = (1e-15, 1.))
        diff = Comparator()
        diff.compare(contribution, reconstruction)
        return contribution


class TestEstimate(unittest.TestCase, Estimate):

    def setUp(self):
        self.infile = 'input-data/Pythia-LHC16-a5.root'
        # self.infile = 'input-data/scaled-LHC17f8a.root'
        self.mc_selection = 'MCStudyOnlyTender'
        self.nonlin_selection = 'PhysNonlinTender'
        self.hname = 'MassPt_#pi^{0}'


    def testContributions(self):
        reconstruction = self.get_hist('MassPt', self.nonlin_selection, 'reconstructed')
        
        # self.estimate('feeddown K^{s}_{0}', reconstruction)
        secondary = self.estimate('secondary ', reconstruction)
        feeddown = self.estimate('feeddown ', reconstruction)

        diff = Comparator()
        diff.compare(secondary, feeddown)

