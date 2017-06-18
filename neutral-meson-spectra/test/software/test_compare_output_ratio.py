
import unittest
import ROOT
import json

import spectrum.comparator as cmpr
from spectrum.sutils import wait, get_canvas

from test.software.test_compare import get_spectrum



class TestOutputRatio(unittest.TestCase):
    """
         This test is needed to check if comparator returns ratio histogram correctly
         or none object when it's not relevant.
    """


    def setUp(self):
        with open('config/test_particles.json') as f: 
            particles = json.load(f)
        self.data = [get_spectrum(i, *particles[i]) for i in particles]

        for h in self.data:
            h.SetTitle("Checking ratio output")


    def testCompareTwo(self):
        diff = cmpr.Comparator()

        self.data[2].SetTitle('Checking output ratio comparator')
        ratio = diff.compare(self.data[2], self.data[1])

        c1 = get_canvas()
        c1.SetLogy(0)
        if ratio:
            ratio.Draw()

        wait("test", True, False)


    def testCompareMultiple(self):
        diff = cmpr.Comparator()

        self.data[0].SetTitle('Checking output ratio comparator')
        ratio = diff.compare(zip(*[self.data, self.data]))
        self.assertFalse(all(ratio))




