import unittest
import ROOT

from spectrum.spectrum import Spectrum
from spectrum.input import Input
from spectrum.sutils import get_canvas, ticks
from spectrum.options import Options


class CrystalBallParametersPi0(unittest.TestCase):
    """
        General idea: Don't use dynamic crystal ball parameters. Use fixed 
        values (not necessarily the same for) the different p_T slices.
        Use this code to estimate values of those parameters. Then move these parameters to the code.
    """

    def setUp(self):
        self.inp = Input('input-data/LHC16.root', 'PhysTender').read()
        self.particle = 'pi0'
        spectrum = Spectrum(self.inp, label='relaxedcb parameters', mode='q', options=Options(relaxedcb=True, particle=self.particle))
        self.alpha, self.n = spectrum.evaluate()[-2:]


    def fitConstant(self, hist, ofile):
        canvas = ROOT.TCanvas('cbfit', 'cbfit', 128 * 6 / 2, 96 * 6)
        ticks(canvas)

        hist.Fit('pol0', 'q')
        hist.SetLineColor(37)
        function = hist.GetFunction('pol0')
        function.SetLineColor(46)

        print hist.GetTitle(), function.GetParameter(0)
        function.Draw('same')
        canvas.Update()
        canvas.SaveAs(ofile)
        raw_input('Press enter to continue')


    def testConstant(self):
        self.fitConstant(self.alpha, 'results/cb-alpha-fit.pdf')
        self.fitConstant(self.n, 'results/cb-n-fit.pdf')


    def tearDown(self):
        """
            Invoke this method to plot the final result 
            only after all previous tests.

            Use values of CB parameters estimated by testConstant method
            to run the comparison.
        """

        c1 = get_canvas(1./2)
        g = lambda x, y, z, w: Spectrum(x, label=y, mode=z, options=w).evaluate()

        infile = 'input-data/LHC16.root'

        results = [
                        g(self.inp, 'fixed cb parameters', 'q', Options(relaxedcb = False, particle=self.particle)),
                        g(self.inp, 'relaxed cb parameters', 'q', Options(relaxedcb = True, particle=self.particle))
                  ]

        import spectrum.comparator as cmpr
        diff = cmpr.Comparator(size=(1./2, 1))
        diff.compare_set_of_histograms(results)


class CrystalBallParametersEta(CrystalBallParametersPi0):
    """
        General idea: Don't use dynamic crystal ball parameters. Use fixed 
        values (not necessarily the same for) the different p_T slices.
        Use this code to estimate values of those parameters. Then move these parameters to the code.
    """

    def setUp(self):
        self.inp = Input('input-data/LHC16.root', 'EtaTender').read()
        self.particle = 'eta'
        spectrum = Spectrum(self.inp, label='relaxedcb parameters', mode='q', options=Options(relaxedcb=True, particle=self.particle))
        self.alpha, self.n = spectrum.evaluate()[-2:]


