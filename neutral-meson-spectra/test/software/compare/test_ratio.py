
import unittest
import ROOT

import spectrum.comparator as cmpr
from particles import Particles

def get_fit_function():
    func_nonlin = ROOT.TF1("func_nonlin", "pol2(0) + pol1(3)", 0, 100);
    func_nonlin.SetParLimits(0, -10, 0)
    func_nonlin.SetParameter(0, -1.84679e-02)
    func_nonlin.SetParameter(1, -4.70911e-01)
    func_nonlin.SetParameter(2, -4.70911e-01)

    func_nonlin.SetParameter(3, 0.35)
    func_nonlin.SetParameter(4, 0.78)
    return func_nonlin


class TestRatio(unittest.TestCase, Particles):

    def setUp(self):
        self.data, self.stop = self.config()

    def testCompareTwo(self):
        diff = cmpr.Comparator(stop = self.stop)
        self.data[2].SetTitle('Comparing double plots')
        diff.compare(self.data[2], self.data[1])


    def testCompareRatio(self):
        diff = cmpr.Comparator(stop = self.stop)
        main = self.data[1]
        main.SetTitle('Testing yaxis maximal range for off scale points')
        distorted = main.Clone(main.GetName() + '_clone')
        distorted.SetBinContent(80, distorted.GetBinContent(80) * 100)
        distorted.label = 'distorted'
        diff.compare(main, distorted)


    def testCompareTwoWithFit(self):
        """
            Checks multiple fitting ranges. 
        """
   
        title = 'Comparing different ratiofit ranges {!r}'
        ranges = (0, 0), (0, 10), (10, 5), (4, 8)

        for frange in ranges:
            self.data[2].SetTitle(title.format(frange))
            self.data[2].fitfunc = ROOT.TF1('f1', 'pol1(0)', *frange)
            diff = cmpr.Comparator(stop = self.stop)
            diff.compare(self.data[2], self.data[1])


    def testCompareNonlinear(self):
        diff = cmpr.Comparator(stop = self.stop)
        # diff.compare(self.data[2], self.data[1])

        self.data[0].SetTitle('Comparing nonlinear fit function')
        self.data[0].fitfunc = get_fit_function()
        diff.compare(self.data[0], self.data[1])


    def testRebin(self):
        diff = cmpr.Comparator(stop = self.stop)
        # diff.compare(self.data[2], self.data[1])

        self.data[0].SetTitle('Test Rebin Function second')
        self.data[0].Rebin(2)
        diff.compare(self.data[0], self.data[1])

        self.data[0].SetTitle('Test Rebin Function first')
        self.data[1].Rebin(2)
        diff.compare(self.data[0], self.data[1])

    def test_ignore_ratio_plot(self):
        diff = cmpr.Comparator(stop = self.stop)

        self.data[0].SetTitle('Test ignore ratio plot: This should be OK')
        diff.compare(self.data[0], self.data[1])

        diff = cmpr.Comparator(rrange = (-1, -1), stop = self.stop)

        self.data[0].SetTitle('Test ignore ratio plot: This plot should be without ratio pad')
        diff.compare(self.data[0], self.data[1])

