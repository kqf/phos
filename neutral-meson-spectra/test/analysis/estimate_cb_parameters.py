import unittest
import ROOT

from spectrum.spectrum import Spectrum
from spectrum.input import Input
from spectrum.sutils import get_canvas
from spectrum.options import Options


class CrystalBallParameters(unittest.TestCase):
    """
        General idea: Don't use dynamic crystal ball parameters. Use fixed 
        values (not necessarily the same for) the different p_T slices.
        Use this code to estimate values of those parameters. Then move these parameters to the code.
    """

    def setUp(self):
        infile = 'input-data/LHC16.root'
        spectrum = Spectrum(Input(infile, 'PhysTender').read(), label='fixed cb parameters', mode='q', options=Options(relaxedcb=True))
        self.mass, self.width, self.spectrum, self.chi2, self.alpha, self.n = spectrum.evaluate()


    def fitConstant(self, hist, ofile):
        canvas = ROOT.TCanvas('cbfit', 'cbfit', 128 * 6 / 2, 96 * 6)
        canvas.SetTickx()
        canvas.SetTicky()
        canvas.SetGridy()
        canvas.SetGridx()

        hist.Fit('pol0', 'q')
        hist.SetLineColor(37)
        function = hist.GetFunction('pol0')
        function.SetLineColor(46)
        function.Draw('same')
        canvas.Update()
        canvas.SaveAs(ofile)
        raw_input()


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
        g = lambda x, y, z, w: Spectrum(x, label=y, mode=z, options=w).evaluate()

        infile = 'input-data/LHC16.root'

        c1 = get_canvas(1./2)

        results = [
                   g(Input(infile, 'PhysTender').read(), 'fixed cb parameters', 'q', Options(relaxedcb = False)), 
                   g(Input(infile, 'PhysTender').read(), 'relaxed cb parameters', 'q', Options(relaxedcb = True))
                  ]

        import spectrum.comparator as cmpr
        diff = cmpr.Comparator()
        diff.compare_set_of_histograms(results)






