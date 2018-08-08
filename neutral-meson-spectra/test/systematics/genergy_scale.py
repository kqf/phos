import unittest
from spectrum.broot import BROOT as br
from uncertainties.genergy_scale import GlobalEnergyScaleUncetanityEvaluator


# CWR: Run this on corrected spectrum
#
class TestGE(unittest.TestCase):

    def test_systematics(self):
        spectrum, lower, upper = GlobalEnergyScaleUncetanityEvaluator().fit()
        syst_error = self.outsys.histogram(spectrum)
        bins = [syst_error.GetBinCenter(i) for i in br.range(syst_error)]
        bins = [upper.Eval(c) - lower.Eval(c) for c in bins]
        for i, b in enumerate(bins):
            if b < 0:
                print 'Warning: negative global energy scale corrections'
            syst_error.SetBinContent(i + 1, abs(b))
        return syst_error
