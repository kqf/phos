import ROOT
import unittest
import os
import random

from drawtools.style import Styler


# Use multiple inheritance to avoid
# problem of calling tests from parent classes
#

class GeneralTest(object):
    def __init__(self):
        super(GeneralTest, self).__init__()
        self.conffile = None

    def testDrawing(self):
        style = Styler(self.conffile)
        style.draw()

    def fill_random(self, histogram, pars):
        if type(histogram) is ROOT.TH1F:
            return self.fill_random1d(histogram, pars)

        self.fill_random2d(histogram, pars)

    def fill_random1d(self, histogram, pars):
        f1 = ROOT.TF1(
            'mfunc', "TMath::Exp( -1 * (x - [0]) * (x - [0]) / [1] / [1] )")
        f1.SetParameter(0, pars[0] * 2 * pars[0])
        f1.SetParameter(1, 3 - pars[1])
        histogram.FillRandom('mfunc', 10000)

    def fill_random2d(self, histogram, pars):
        xaxis, yaxis = histogram.GetXaxis(), histogram.GetYaxis()

        def iterate(x):
            return range(1, x.GetNbins() + 1)

        for i in iterate(xaxis):
            for j in iterate(yaxis):
                histogram.SetBinContent(i, j, random.randint(1, 5))


class TestImages(unittest.TestCase):

    def setUp(self):
        # Different values in some pt-bins can be explained by limited statistics in those bins.
        #
        # This one should be changed later
        self.conffile, self.infile, histname = self.save_config()
        self.save_histogram(self.infile, histname)

        # TOOD: Add --save_config command line option

    def save_config(self):
        pass

    def save_histogram(self):
        pass

    def tearDown(self):
        os.remove(self.conffile)
        os.remove(self.infile)
