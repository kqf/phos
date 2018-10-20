import ROOT
import spectrum.sutils as sl
from spectrum.broot import BROOT as br
from spectrum.comparator import Comparator
from spectrum.corrected_yield import CorrectedYield
from spectrum.transformer import TransformerBase
from spectrum.pipeline import ReduceArgumentPipeline
from spectrum.pipeline import Pipeline
from vault.formulas import FVault


# CWR: Run this on corrected spectrum
#

class MockEpRatio(TransformerBase):
    def transform(self, data, loggs):
        return 0.01


class TsallisFitter(TransformerBase):
    @classmethod
    def fitfunc(klass, name='', bias=0.0001):
        fitf = ROOT.TF1(name, FVault().func("tsallis"), 2, 25)
        fitf.SetParameter(0, 2.40)
        fitf.SetParameter(1, 0.139)
        fitf.SetParameter(2, 6.88)
        return fitf

    def transform(self, corrected_yield, loggs):
        fitf = self.fitfunc('tsallis_')
        corrected_yield.Fit(fitf, 'R', '')
        # corrected_yield.Draw()
        # diff = Comparator(stop=self.plot)
        # diff.compare(corrected_yield)
        corrected_yield.fitf = fitf
        return [(corrected_yield, fitf)]


class GScale(TransformerBase):

    def __init__(self, options, plot=True):
        super(GScale, self).__init__(plot)
        self.options = options
        # This should be studied on corrected yield
        self.pipeline = ReduceArgumentPipeline(
            Pipeline([
                ("cyield", CorrectedYield(options)),
                ("tsallis_fit", TsallisFitter()),
            ]),
            MockEpRatio(options),
            self.fit
        )

    @staticmethod
    def ratiofunc(fitf, name='', bias=0.01, color=46):
        def rf(x, p):
            tsallis = ROOT.TF1("f", FVault().func("tsallis"), 0, 100)
            tsallis.SetParameters(*p)
            return tsallis.Eval(x[0] + x[0] * bias) / tsallis.Eval(x[0])
        rfunc = ROOT.TF1(name, rf, 0, 25, 3)
        pars, _ = br.pars(fitf)
        rfunc.SetParameters(*pars)
        rfunc.SetLineColor(color)
        return rfunc

    def fit(self, data, ep_ratio):
        corrected_yield, fitf = data
        lower = self.ratiofunc(fitf, 'low', -0.01, 38)
        upper = self.ratiofunc(fitf, 'up', 0.01, 47)

        # diff = Comparator(stop=self.plot, rrange=(-1, ), crange=(0.9, 1.1))
        # diff.compare(
        #     lower.GetHistogram(),
        #     upper.GetHistogram()
        # )

        syst_error = corrected_yield.Clone("gescale")
        bins = [syst_error.GetBinCenter(i) for i in br.range(syst_error)]
        bins = [lower.Eval(c) - upper.Eval(c) for c in bins]
        for i, b in enumerate(bins):
            if b < 0:
                print 'Warning: negative global energy scale corrections'
            syst_error.SetBinContent(i + 1, abs(b))
        return syst_error
