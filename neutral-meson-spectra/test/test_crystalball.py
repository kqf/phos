import unittest

class Test(unittest.TestCase):

    def setUp(self):
        self.names = ("alpha", "n", "a", "b")
        self.expected = (1.1, 2.0, 1.8052047161643283, 0.718181818181818)

    def testCBParameters(self):
        # Just to be sure that parameters didn't change accidentally
        from spectrum.parametrisation import CrystalBall
        actual = CrystalBall((0, 0)).cb_parameters()
        for a, b, c in zip(self.expected, actual, self.names): 
            self.assertAlmostEqual(a, b, msg="Failed parameter " + c + ": %0.7f != %0.7f" % (a, b))
