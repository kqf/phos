
import sys
import unittest
import ROOT

from spectrum.spectrum import Spectrum
from spectrum.input import Input
from spectrum.invariantmass import InvariantMass
from spectrum.sutils import wait
from spectrum.options import Options



class TestInvariantMassClass(unittest.TestCase):

    def setUp(self):
        self.wait = 'discover' not in sys.argv 
        self.input = Input('input-data/LHC16.root', 'PhysTender').read()
        self.particles = {
                            'pi0': ((8, 9), 0)
                           ,'eta': ((0.8, 1.4), 5)
                         }

    def draw(self, particle, func, title):
        bin, nrebin = self.particles[particle]
        mass = InvariantMass(self.input, bin, nrebin, Options(particle=particle))
        mass.extract_data()
        func(mass)
        wait('test-inmass-%s-' % particle + title , self.wait, True)

    # @unittest.skip('')
    def testDrawSignal(self):
        f = lambda x: x.draw_signal()

        for p in self.particles: 
            self.draw(p, f, 'signal')

    # @unittest.skip('')
    def testDrawRatio(self):
        f = lambda x: x.draw_ratio()

        for p in self.particles: 
            self.draw(p, f, 'ratio')

    # @unittest.skip('')
    def testDrawMass(self):
        f = lambda x: x.draw_mass()

        for p in self.particles: 
            self.draw(p, f, 'mass')


    def draw_multiple(self, particle):
        option = Options(
                            particle = particle, 
                            label = 'test-' + particle, 
                            mode  =  'q'
                         )
        analysis = Spectrum(self.input, option)
        analysis.evaluate()
        pt = analysis.analyzer
        pt.show_img = True
        intgr_ranges = [None] * len(pt.masses)
        pt.draw_ratio(intgr_ranges)
        pt.draw_mass(intgr_ranges)
        pt.draw_signal(intgr_ranges)

    def testMultiplePlots(self):
        for p in self.particles: 
            self.draw_multiple(p)

