import ROOT
import spectrum.sutils as sl
from spectrum.broot import BROOT as br
from spectrum.comparator import Comparator
from spectrum.corrected_yield import CorrectedYield
from spectrum.transformer import TransformerBase


# CWR: Run this on corrected spectrum
#

class GlobalEnergyScaleUncetanityEvaluator(TransformerBase):

    def __init__(self, options, stop=True):
        super(GlobalEnergyScaleUncetanityEvaluator, self).__init__(stop)
        self.options
        # This should be studied on corrected yield

    @staticmethod
    def ratiofunc(fitf, name='', bias=0.01, color=46):
        def rf(x, p):
            return sl.tsallis(
                [x[0] + x[0] * bias], p) / sl.tsallis(x, p)
        rfunc = ROOT.TF1(name, rf, 0, 25, 3)
        pars, _ = br.pars(fitf)
        rfunc.SetParameters(*pars)
        rfunc.SetLineColor(color)
        return rfunc

    @classmethod
    def fitfunc(klass, name='', bias=0.0001):
        fitf = ROOT.TF1(
            name, lambda x, p: x[0] * sl.tsallis(x, p, bias=bias), 2, 25, 3)
        fitf.SetParameter(0, 2.40)
        fitf.SetParameter(1, 0.139)
        fitf.SetParameter(2, 6.88)
        return fitf

    def fit(self):
        corrected_spectrum = CorrectedYield(self.options).transform(data)
        fitf = self.fitfunc('tsallis_')
        corrected_spectrum.Fit(fitf, 'R', '')
        corrected_spectrum.Draw()

        diff = Comparator(stop=self.stop)
        diff.compare(corrected_spectrum)

        lower = self.ratiofunc(fitf, 'low', -0.01, 38)
        upper = self.ratiofunc(fitf, 'up', 0.01, 47)

        diff = Comparator(stop=self.stop, rrange=(-1, ), crange=(0.9, 1.1))
        diff.compare(
            lower.GetHistogram(),
            upper.GetHistogram()
        )

        return corrected_spectrum, lower, upper

    def transform(self, data):
        spectrum, lower, upper = self.fit(data)
        syst_error = self.outsys.histogram(spectrum)
        bins = [syst_error.GetBinCenter(i) for i in br.range(syst_error)]
        bins = [upper.Eval(c) - lower.Eval(c) for c in bins]
        for i, b in enumerate(bins):
            if b < 0:
                print 'Warning: negative global energy scale corrections'
            syst_error.SetBinContent(i + 1, abs(b))
        return syst_error
