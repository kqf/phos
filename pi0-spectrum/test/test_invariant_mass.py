
import unittest
import ROOT

from spectrum.spectrum import PtAnalyzer
from spectrum.input import Input
from spectrum.InvariantMass import InvariantMass

class TestInvariantMassClass(unittest.TestCase):

	def testDrawOption(self):
		nevents, real, mix = Input('input-data/LHC16l.root', 'PhysTender').read()

		mass = InvariantMass(real, mix, (0.8, 1.0))
		print mass.extract_data()
		mass.extract_data()
		mass.draw_ratio()
		mass.draw_mass()
		mass.draw_signal()


		# second = PtAnalyzer(Input('input-data/LHC16l.root', 'PhysTender').read(), label = 'Mixing', mode = 'q').quantities()
		# actual = [ [ h.GetBinContent(i) for i in range(1, h.GetNbinsX())] for h in second]

		# for a, b, c in zip(nominal, actual, second):
				# print 'Checking ', c.GetName()
				# for aa, bb in zip(a, b): self.assertAlmostEqual(aa, bb)