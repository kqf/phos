import unittest
import ROOT

from spectrum.spectrum import Spectrum
from spectrum.input import Input
from spectrum.sutils import get_canvas


class CrystalBallParameters(unittest.TestCase):
    """
        General idea: Don't use dynamic crystal ball parameters. Use fixed 
        values (not necessarily the same for) the different p_T slices.
        Use this code to estimate values of those parameters. Then move these parameters to the code.
    """

    def setUp(self):
        infile = 'input-data/LHC16.root'
        spectrum = Spectrum(Input(infile, 'PhysTender').read(), label='fixed cb parameters', mode='q', relaxedcb=True)
        self.mass, self.width, self.spectrum, self.chi2, self.alpha, self.n = spectrum.evaluate()


    def testLinear(self):
        # TODO: save the images
        
        canvas = get_canvas()
        canvas.Clear()
        canvas.Divide(2, 1)

        canvas.cd(1)
        self.alpha.Fit('pol0')
        self.alpha.SetLineColor(37)
        function = self.alpha.GetFunction('pol0')
        function.SetLineColor(46)

        canvas.cd(2)
        self.n.Draw()
        self.n.SetLineColor(37)
        self.n.Fit('pol0')
        function = self.n.GetFunction('pol0')
        function.SetLineColor(46)

        canvas.Update()
        raw_input()


