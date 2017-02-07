
import unittest

class Test(unittest.TestCase):

	def testCBParameters(self):
		# Just to be that parameters didn't change accidentally
		from spectrum.CrystalBall import CBParameters
		names = ("alpha", "n", "a", "b")
		expected = (1.1, 2.0, 1.8052047161643283, 0.718181818181818)
		actual = CBParameters()
		for a, b, c in zip(expected, actual, names): 
			self.assertAlmostEqual(a, b, msg="Failed parameter " + c + ": %0.7f != %0.7f" % (a, b))

