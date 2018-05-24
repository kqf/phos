
from spectrum.comparator import Comparator
from spectrum.input import read_histogram

import ROOT
import os.path
import unittest

from spectrum.broot import BROOT as br


class InspectSources(unittest.TestCase):

    def setUp(self):
        # self.infile = 'input-data/Pythia-LHC16-a5.root'
        self.infile = 'scaled-LHC17f8a'
        self.selection = 'MCStudyOnlyTender'
        self.particles_set = {
            'primary': ['', '#rho^{+}', '#rho^{-}', 'K^{s}_{0}', '#Lambda', '#pi^{+}', '#pi^{-}', '#eta', '#omega', 'K^{*+}', 'K^{*-}', 'K^{*0}', '#barK^{*0}', 'K^{+}', 'K^{-}', '#Sigma^{0}'],
            'secondary': ['', 'K^{s}_{0}', '#Lambda', '#pi^{+}', '#pi^{-}', '#eta', '#omega'],
            'feeddown': ['', 'K^{s}_{0}', '#Lambda', '#pi^{+}', '#pi^{-}', '#eta', '#omega']
        }

    def get_baseline(self):
        generated = read_histogram(
            self.infile, self.selection, 'hPt_#pi^{0}', 'generated', norm=True)
        br.scalew(generated)
        return generated

    def inspect(self, ptype):
        def f(x):
            return read_histogram(
                self.infile, self.selection,
                'hPt_#pi^{0}_%s_%s' % (ptype, x), x if x else 'all', norm=True)
        particles = map(f, self.particles_set[ptype])
        map(br.scalew, particles)

        for p in particles:
            p.logy = True

        generated = self.get_baseline()
        diff = Comparator(crange=(1e-15, 1.),
                          oname='{0}_spectrum_{1}'.format(ptype, self.infile))
        diff.compare(particles)

        diff = Comparator(crange=(1e-15, 1.),
                          oname='{0}_ratio_{1}'.format(ptype, self.infile))
        diff.compare_ratios(particles, generated, logy=True)

        diff = Comparator(crange=(1e-15, 1.),
                          oname='{0}_sum{1}'.format(ptype, self.infile))
        total, summed = particles[0], br.sum(particles[1:], 'sum')
        diff.compare(total, summed)

    # @unittest.skip('')
    def testContributions(self):
        # self.inspect('secondary')
        # self.inspect('primary')
        self.inspect('feeddown')

    # Use this test to compare efficiencies calculated from all particles and from primaries.
    # These efficiencies will differ only by denominators
    def testComparePrimaryEfficiency(self):
        generated = read_histogram(
            self.infile, self.selection, 'hPt_#pi^{0}', 'all', norm=True)
        primaries = read_histogram(
            self.infile,
            self.selection,
            'hPt_#pi^{0}_primary_', 'primary', norm=True)

        diff = Comparator(oname='{0}-primaries-to-all-generated-ratio.pdf')
        diff.compare(primaries, generated)
