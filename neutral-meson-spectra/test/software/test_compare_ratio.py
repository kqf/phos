
import unittest
import ROOT
import json

import spectrum.comparator as cmpr
from test.software.test_compare import get_spectrum

def get_fit_function():
    func_nonlin = ROOT.TF1("func_nonlin", "pol2(0) + pol1(3)", 0, 100);
    func_nonlin.SetParLimits(0, -10, 0)
    func_nonlin.SetParameter(0, -1.84679e-02)
    func_nonlin.SetParameter(1, -4.70911e-01)
    func_nonlin.SetParameter(2, -4.70911e-01)

    func_nonlin.SetParameter(3, 0.35)
    func_nonlin.SetParameter(4, 0.78)
    return func_nonlin



class Test(unittest.TestCase):

    def setUp(self):
        with open('config/test_particles.json') as f: 
            particles = json.load(f)
        self.data = [get_spectrum(i, *particles[i]) for i in particles]


    @unittest.skip('')
    def testCompareTwo(self):
        diff = cmpr.Comparator()
        self.data[2].SetTitle('Comparing double plots')
        diff.compare_set_of_histograms([[self.data[2]], [self.data[1]]])


    @unittest.skip('')
    def testCompareRatio(self):
        diff = cmpr.Comparator()
        main = self.data[1]
        main.SetTitle('Testing yaxis maximal range for off scale points')
        distorted = main.Clone(main.GetName() + '_clone')
        distorted.SetBinContent(80, distorted.GetBinContent(80) * 100)
        distorted.label = 'distorted'
        diff.compare_set_of_histograms([[main], [distorted]])


    @unittest.skip('')
    def testCompareTwoWithFit(self):
        """
            Checks multiple fitting ranges. 
        """
   
        self.data[2].SetTitle('Comparing different ratiofit ranges')
        diff = cmpr.Comparator(ratiofit=(0, 0))
        diff.compare_set_of_histograms([[self.data[2]], [self.data[1]]])

        diff = cmpr.Comparator(ratiofit=(0, 10))
        diff.compare_set_of_histograms([[self.data[2]], [self.data[1]]])

        diff = cmpr.Comparator(ratiofit=(5, 10))
        diff.compare_set_of_histograms([[self.data[2]], [self.data[1]]])

        diff = cmpr.Comparator(ratiofit=(5, 0))
        diff.compare_set_of_histograms([[self.data[2]], [self.data[1]]])


    @unittest.skip('')
    def testCompareNonlinear(self):
        diff = cmpr.Comparator()
        # diff.compare_set_of_histograms([[self.data[2]], [self.data[1]]])

        self.data[0].SetTitle('Comparing nonlinear fit function')
        self.data[0].fitfunc = get_fit_function()
        diff.compare_set_of_histograms([[self.data[0]], [self.data[1]]])

    def testRebin(self):
        diff = cmpr.Comparator()
        # diff.compare_set_of_histograms([[self.data[2]], [self.data[1]]])

        self.data[0].SetTitle('Test Rebin Function second')
        self.data[0].Rebin(2)
        diff.compare_set_of_histograms([[self.data[0]], [self.data[1]]])

        self.data[0].SetTitle('Test Rebin Function first')
        self.data[1].Rebin(2)
        diff.compare_set_of_histograms([[self.data[0]], [self.data[1]]])

