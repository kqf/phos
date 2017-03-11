
import unittest
import ROOT

from spectrum.spectrum import PtAnalyzer
from spectrum.input import Input
from spectrum.invariantmass import InvariantMass
from spectrum.sutils import wait

class TestInvariantMassClass(unittest.TestCase):

    def testDrawOption(self):
        real_and_mix = Input('input-data/LHC16.root', 'PhysTender').read()

        mass = InvariantMass(real_and_mix, (8., 9.), 0, True, 0, False)
        mass.extract_data()

        mass.draw_ratio()
        wait('inmass-test-ratio', True, True)

        mass.draw_mass()
        wait('inmass-test-mass', True, True)
        
        mass.draw_signal()
        wait('inmass-test-signal', True, True)


    def testMultiplePlots(self):
        f = lambda x, y, z: PtAnalyzer(x, label=y, mode=z)
        infile = 'input-data/LHC16.root'
        analyzer = f(Input(infile, 'PhysTender').read(), 'strict', 'q')
        analyzer.quantities()