import unittest
import ROOT

from spectrum.spectrum import Spectrum
from spectrum.input import Input
from spectrum.sutils import get_canvas, wait
from spectrum.options import Options


class TestMass(unittest.TestCase):
    """
        Use this code to determine the best matching parametrization for area approximation
    """

    def setUp(self):
        self.canvas = get_canvas(1./ 2)
        infile = 'input-data/LHC16.root'
        self.input = Input(infile, 'EtaTender').read()
        self.analysis = Spectrum(self.input, label='fixed cb parameters', mode='q', options=Options(particle='eta', relaxedcb=True))
        self.mass, self.width, self.spectrum, self.chi2, self.alpha, self.n = self.analysis.evaluate()
        self.target = self.mass
        self.models = {
                         "TMath::Exp([0] + [1] * x ) * [2] * x + [3]": [-0.9383877408174801, -7.313302813528194, -102.88494983600319, 0.5590698449654556]
                        ,"[0] + 0 * [1]": [0.558684, 0]
                       }


    def check_parameterisation(self, func, pars):
        self.canvas = get_canvas(1. / 2)
        self.canvas.Clear()

        function = ROOT.TF1('f', func)
        function.SetParameters(*pars)
        function.SetLineColor(46)
        self.target.SetLineColor(37)

        self.target.Fit(function)

        pars = [function.GetParameter(i) for i in range(function.GetNpar())]
        print 'Estimated parameters for {0} :'.format(func), pars
        wait('')

    def testParametrisation(self):
        for f, p in self.models.iteritems():
            self.check_parameterisation(f, p)


    def testCompareDifferentModels(self):
        results = []
        for f, p in self.models.iteritems():
            self.analysis.mass_func = f
            self.analysis.mass_pars = p 
            results.append(self.analysis.evaluate())


        import spectrum.comparator as cmpr
        diff = cmpr.Comparator()
        diff.compare_set_of_histograms(results)


class TestWidth(TestMass):

    def setUp(self):
        super(TestWidth, self).setUp()
        self.target = self.width
        self.models = {
                         "TMath::Exp([0] + [1] * x ) * [2] * x + [3]": [0.2629952468139744, -2.331651575377617, -0.1217264515698897, 0.014533326264109624]
                        ,"[0] + 0 * [1]":  [0.012009189559948466, 0]
                       }


