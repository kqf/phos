import ROOT

import spectrum.broot as br
from spectrum.analysis import Analysis
from spectrum.pipeline import TransformerBase
from spectrum.options import Options
from spectrum.pipeline import Pipeline, HistogramSelector
from spectrum.pipeline import FitfunctionAssigner
from spectrum.pipeline import RebinTransformer
from spectrum.pipeline import OutputDecorator
from spectrum.pipeline import ReducePipeline
from spectrum.pipeline import ParallelPipeline
from spectrum.comparator import Comparator
from spectrum.tools.unityfit import unityfit
from spectrum.plotter import plot
from vault.datavault import DataVault


def tof_data():
    return (
        DataVault().input("data", "tof", histname="MassPtSM0"),
        DataVault().input("data", "isolated", histname="MassPtSM0"),
    )


def tof_data_stable():
    return (
        DataVault().input("data", "stable"),
        DataVault().input("data", "isolated", histname="MassPtSM0"),
    )


def report(func):
    print(r"\def \uncertaintyTofChi {{{val:.3g}}}".format(
        val=br.chi2ndff(func)
    ))
    print(r"\def \uncertaintyTof {{{val:.3g}}}".format(
        val=func.GetParameter(0)
    ))
    print(r"\def \uncertaintyTofError {{{val:.3g}}}".format(
        val=func.GetParError(0)
    ))
    xmin, xmax = ROOT.Double(0), ROOT.Double(0)
    func.GetRange(xmin, xmax)
    print(r"\def \uncertaintyTofLowPt {{{val:.3g}}}".format(
        val=xmin
    ))
    print(r"\def \uncertaintyTofHighPt {{{val:.3g}}}".format(
        val=xmax
    ))


def tof_ratio(histograms, loggs, fitf):
    for i in br.hrange(histograms[1]):
        if histograms[1].GetBinContent(i) < 0:
            histograms[1].SetBinContent(i, abs(histograms[1].GetBinContent(i)))

    histograms[0].SetTitle("12.5 ns cut")
    histograms[1].SetTitle("no cut")

    plot(
        histograms,
        logy=True,
        logx=True,
        xtitle="p_{T} (GeV/#it{c})",
        csize=(96, 128),
        oname="results/systematics/tof/yields.pdf",
        more_logs=False,
        yoffset=1.6,
    )
    ratio = Comparator(stop=False).compare(histograms)
    ratio.Fit(fitf, "R")
    ratio.SetTitle("Data")
    fitf.SetTitle("Constant fit")
    fitf.SetLineStyle(9)
    fitf.SetLineColor(ROOT.kBlack)
    report(fitf)

    plot(
        [ratio, fitf],
        logy=False,
        logx=True,
        ytitle="R_{TOF}",
        xtitle="p_{T} (GeV/#it{c})",
        xlimits=(0.8, 9.6),
        ylimits=(0, 2.5),
        csize=(96, 128),
        oname="results/systematics/tof/ratios.pdf",
        more_logs=False,
    )
    return ratio


class TofUncertaintyOptions(object):

    def __init__(self, particle="#pi^{0}"):
        super(TofUncertaintyOptions, self).__init__()
        self.data = Options()
        self.isolated = Options()
        self.decorate = self.data.particle, "isolated"
        self.fit_range = 1.0, 7.5
        self.fitf = ROOT.TF1("ratio", "1. - pol0(0)", *self.fit_range)
        self.fitf.SetParameter(0, 0.02)
        self.edges = None
        if particle != "#pi^{0}":
            self.edges = Options(particle=particle).pt.ptedges


class RatioFitter(TransformerBase):
    title = "TOF uncertainty; p_{T} (GeV/#it{c}); Relateive error, %"

    def __init__(self, fit_range, plot=False):
        super(RatioFitter, self).__init__(plot)
        self.fit_range = fit_range

    def transform(self, ratio, loggs):
        return unityfit(ratio, self.title, self.fit_range)


class RangeSetter(TransformerBase):
    def __init__(self, fit_range):
        self.fit_range = fit_range

    def transform(self, hist, loggs):
        hist.GetXaxis().SetRangeUser(*self.fit_range)
        return hist


class TofUncertainty(TransformerBase):

    def __init__(self, options, plot=False):
        super(TofUncertainty, self).__init__(plot)
        estimators = [
            ('25ns', Pipeline([
                ("reconstruction", Analysis(options.data, plot)),
                ("spectrum", HistogramSelector("spectrum", plot)),
                ("range", RangeSetter(options.fit_range)),
                ("FitF", FitfunctionAssigner(options.fitf, plot)),
            ])),
            ('isolated', Pipeline([
                ("ReconstructMesons", Analysis(options.isolated, plot)),
                ("spectrum", HistogramSelector("spectrum", plot)),
                ("range", RangeSetter(options.fit_range)),
                ("decorate", OutputDecorator(*options.decorate)),
            ])),
        ]

        # labels = list(zip(*estimators))[0]
        ratio = ReducePipeline(
            ParallelPipeline(estimators),
            lambda x, loggs: tof_ratio(x, loggs, fitf=options.fitf)
        )

        self.pipeline = Pipeline([
            ("spectrum_isolated_spectra_ratio", ratio),
            ("pol0_fit", RatioFitter(options.fit_range)),
            ("rebin", RebinTransformer(True, options.edges)),
        ])
