from __future__ import print_function

import ROOT
import spectrum.broot as br
import spectrum.sutils as su
from spectrum.pipeline import TransformerBase
from spectrum.corrected_yield import CorrectedYield
from spectrum.options import CompositeCorrectedYieldOptions
from spectrum.options import DataMCEpRatioOptions
from spectrum.pipeline import ReduceArgumentPipeline
from spectrum.pipeline import FunctionTransformer
from spectrum.pipeline import Pipeline
from spectrum.plotter import plot
from vault.formulas import FVault

from vault.datavault import DataVault
from spectrum.tools.feeddown import data_feeddown


def ep_data(prod="data", version="latest"):
    return DataVault().input(
        prod,
        version=version,
        listname="EpRatio",
        histname="EpElectronsPSM0",
        use_mixing=False)


def ge_scale_data(particle):
    mcproduction = "single {}".format(particle)
    return (
        (
            ep_data("data", "tof"),
            ep_data("pythia8"),
        ),
        (
            (
                DataVault().input("data", histname="MassPtSM0"),
                data_feeddown(particle == "#eta"),
            ),
            (
                DataVault().input(mcproduction, "low", "PhysEff"),
                DataVault().input(mcproduction, "high", "PhysEff"),
            )
        ),
    )


class GScaleOptions(object):
    def __init__(self, particle="#pi^{0}"):
        self.cyield = CompositeCorrectedYieldOptions(particle=particle)
        self.ep_ratio = DataMCEpRatioOptions()
        self.particle = particle


class MockEpRatio(TransformerBase):
    def transform(self, data, loggs):
        return 0.004


class TsallisFitter(TransformerBase):
    @classmethod
    def fitfunc(klass, name="", bias=0.0001):
        fitf = FVault().tf1("tsallis")
        fitf.SetParameter(0, 2.40)
        fitf.SetParameter(1, 0.139)
        fitf.SetParameter(2, 6.88)
        return fitf

    def transform(self, corrected_yield, loggs):
        fitf = self.fitfunc("tsallis_")
        corrected_yield.Fit(fitf, "RQ")
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
        self.pipeline = Pipeline([
            ("gescale_raw", ReduceArgumentPipeline(
                ("tsallis fit", Pipeline([
                    ("cyield", CorrectedYield(options.cyield)),
                    ("tsallis_fit", TsallisFitter()),
                ])),
                ("E/p ratio", MockEpRatio(options.ep_ratio)),
                self.fit
            )),
            ("gescale", FunctionTransformer(lambda output, loggs: output[0])),
        ])

    @staticmethod
    def ratiofunc(fitf, name="", bias=0.01, color=46):
        def rf(x, p):
            tsallis = ROOT.TF1("f", FVault().func("tsallis"), 0, 100)
            tsallis.SetParameters(*p)
            return tsallis.Eval(x[0] + x[0] * bias) / tsallis.Eval(x[0])
        rfunc = ROOT.TF1(name, rf, 0, 25, 3)
        pars, _ = br.pars(fitf)
        rfunc.SetParameters(*pars)
        rfunc.SetLineColor(color)
        return rfunc

    def fit(self, data, ep_ratio, loggs=None):
        corrected_yield, fitf = data
        lower = self.ratiofunc(fitf, "low", ep_ratio, 38)
        upper = self.ratiofunc(fitf, "up", -ep_ratio, 47)

        upper.SetTitle("f(p_{T} + #delta p_{T})/f(p_{T})")
        upper.SetLineColor(ROOT.kBlue + 1)
        lower.SetTitle("f(p_{T} - #delta p_{T})/f(p_{T})")
        lower.SetLineColor(ROOT.kRed + 1)
        lower.GetXaxis().SetTitle("p_{T} (GeV/#it{c})")
        plot(
            [lower, upper],
            logy=False,
            csize=(96, 128),
            oname="results/systematics/gescale/{}.pdf".format(
                su.spell(self.options.particle)),
            ltitle="{} #rightarrow #gamma #gamma".format(
                self.options.particle
            ),
        )
        syst_error = corrected_yield.Clone("gscale")
        syst_error.Reset()
        syst_error.SetTitle("")
        syst_error.GetYaxis().SetTitle("rel. syst. error")
        syst_error.label = "global energy scale"
        bins = [syst_error.GetBinCenter(i) for i in br.hrange(syst_error)]
        bins = [max(1 - lower.Eval(c), upper.Eval(c) - 1) for c in bins]
        for i, b in enumerate(bins):
            syst_error.SetBinContent(i + 1, b)
        return syst_error
