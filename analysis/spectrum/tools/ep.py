import ROOT
import spectrum.broot as br
from spectrum.processing import DataExtractor
from spectrum.processing import DataPreparator, InvariantMassExtractor
from spectrum.mass import SignalFitExtractor, FitQualityExtractor
from spectrum.pipeline import Pipeline
from spectrum.pipeline import ReducePipeline
from spectrum.pipeline import ParallelPipeline
from spectrum.pipeline import TransformerBase
from spectrum.pipeline import HistogramSelector
from spectrum.pipeline import FitfunctionAssigner
from spectrum.pipeline import AnalysisDataReader
from spectrum.processing import PeakPropertiesEstimator
from spectrum.comparator import Comparator
from spectrum.mass import MassTransformer
from spectrum.plotter import plot


class IdentityExtractor(MassTransformer):
    in_cols = ["measured_fitter", "measured"]
    out_cols = ["signalf", "bgrf", "signal"]
    result_type = "expand"

    def __init__(self, options):
        super(IdentityExtractor, self).__init__()
        self.options = options

    # TODO: Add logging support for the base class
    def apply(self, imass, mass, loggs={}):
        ROOT.gStyle.SetOptFit()
        signal = mass.Clone()
        formula = "gaus(0) + {}(3)".format(self.options.background)
        func = ROOT.TF1("func", formula, *self.options.fit_range)

        func.SetParNames(*self.options.par_names)
        func.SetParameters(*self.options.start_paremeters)
        func.SetLineColor(ROOT.kRed + 1)
        signal.Fit(func, "RQ0")
        bkgrnd = ROOT.TF1("bkgrnd", self.options.background,
                          *self.options.fit_range)
        for i in range(3, func.GetNpar()):
            bkgrnd.SetParameter(i - 3, func.GetParameter(i))
        chi2ndf = func.GetChisquare() / (func.GetNDF() or 1)
        title = ", #chi^{{2}} / ndf = {:.3f}".format(chi2ndf)
        mass.SetTitle(mass.GetTitle() + title)
        signal.SetTitle(signal.GetTitle() + title)
        a, b = self.options.fit_range
        signal.GetXaxis().SetRangeUser(a, b)
        # signal.Scale(1. / signal.Integral())
        loggs.update({signal.GetName(): signal})
        return func, bkgrnd, signal


class EpRatioEstimator(TransformerBase):

    def __init__(self, options, plot=False):
        super(EpRatioEstimator, self).__init__(plot)
        self.pipeline = Pipeline([
            ("read", AnalysisDataReader()),
            ("slice", DataPreparator(options.analysis.pt)),
            ("parametrize", InvariantMassExtractor(options.analysis.invmass)),
            ("fit", IdentityExtractor(options.analysis.invmass.signal)),
            ("massextractor", SignalFitExtractor(in_cols=["signalf"])),
            ("measured_chi", FitQualityExtractor(in_cols=["signalf"])),
            ("ranges", PeakPropertiesEstimator(options.analysis.calibration)),
            ("data", DataExtractor(options.analysis.output)),
            ("ep", HistogramSelector("mass", plot)),
            ("fitf", FitfunctionAssigner(options.fitf, plot)),
        ])


def double_ratio(histograms, loggs, fitf, labels, stop):
    for h, l in zip(histograms, labels):
        h.SetTitle(l)

    plot(
        histograms,
        stop=stop,
        logy=False,
        logx=False,
        xtitle="#it{p}_{T} (GeV/#it{c})",
        csize=(96, 128),
        oname="images/systematics/gescale/ep.pdf",
        more_logs=False,
        yoffset=1.6,
    )
    ratio = Comparator(stop=False).compare(histograms)
    ratio.Fit(fitf, "RQ")
    ratio.SetTitle("Double ratio")
    fitf.SetRange(0.7, 2)
    fitf.SetTitle("Constant fit")
    fitf.SetLineStyle(9)
    fitf.SetLineColor(ROOT.kBlack)
    fitf.SetName("uncertaintyEp")
    fitf.SetParName(0, "")
    br.report(fitf, limits=True)

    plot(
        [ratio, fitf],
        stop=stop,
        logy=False,
        logx=False,
        ytitle="(#it{E}/#it{p})_{Data} / (#it{E}/#it{p})_{MC}",
        xtitle="#it{p}_{T} (GeV/#it{c})",
        csize=(96, 128),
        oname="images/systematics/gescale/double-ep.pdf",
        more_logs=False,
        yoffset=1.6,
    )
    return ratio


class DataMCEpRatioEstimator(TransformerBase):
    def __init__(self, options, plot=False):
        super(DataMCEpRatioEstimator, self).__init__(plot)
        estimators = [
            ("Data", EpRatioEstimator(options.data)),
            ("MC", EpRatioEstimator(options.mc)),
        ]

        labels = list(zip(*estimators))[0]
        self.pipeline = ReducePipeline(
            ParallelPipeline(estimators),
            lambda x, loggs:
                double_ratio(x, loggs, options.data.fitf, labels, stop=plot)
        )
