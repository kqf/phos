import ROOT
import spectrum.broot as br
from spectrum.processing import DataSlicer, InvariantMassExtractor
from spectrum.pipeline import Pipeline
from spectrum.pipeline import ReducePipeline
from spectrum.pipeline import ParallelPipeline
from spectrum.pipeline import TransformerBase
from spectrum.processing import RangeEstimator, DataExtractor
from spectrum.pipeline import HistogramSelector
from spectrum.pipeline import FitfunctionAssigner
from spectrum.comparator import Comparator
from spectrum.plotter import plot


class IdentityExtractor(object):
    def __init__(self, options):
        super(IdentityExtractor, self).__init__()
        self.options = options

    def transform(self, mass, loggs):
        ROOT.gStyle.SetOptFit()
        mass.signal = mass.mass.Clone()
        formula = "gaus(0) + {}(3)".format(self.options.background)
        func = ROOT.TF1("func", formula, *self.options.fit_range)

        func.SetParNames(*self.options.par_names)
        func.SetParameters(*self.options.start_paremeters)
        func.SetLineColor(ROOT.kRed + 1)
        mass.signal.Fit(func, "RQ0")
        bkgrnd = ROOT.TF1("bkgrnd", self.options.background,
                          *self.options.fit_range)
        for i in range(3, func.GetNpar()):
            bkgrnd.SetParameter(i - 3, func.GetParameter(i))
        mass.sigf = func
        mass.bgrf = bkgrnd
        chi2ndf = func.GetChisquare() / (func.GetNDF() or 1)
        title = ", #chi^{{2}} / ndf = {:.3f}".format(chi2ndf)
        mass.mass.SetTitle(mass.mass.GetTitle() + title)
        mass.signal.SetTitle(mass.signal.GetTitle() + title)
        a, b = self.options.fit_range
        mass.signal.GetXaxis().SetRangeUser(a, b)
        # mass.signal.Scale(1. / mass.signal.Integral())
        loggs.update({mass.signal.GetName(): mass.signal})
        return mass


class EpFitter(object):

    def __init__(self, options):
        super(EpFitter, self).__init__()
        self.pipeline = [
            IdentityExtractor(options),
        ]

    def transform(self, masses, loggs):
        local_loggs = {}
        for estimator in self.pipeline:
            for mass in masses["invmasses"].values:
                estimator.transform(mass, local_loggs)
        loggs.update({"epfitter": local_loggs})
        return masses


class EpRatioEstimator(TransformerBase):

    def __init__(self, options, plot=False):
        super(EpRatioEstimator, self).__init__(plot)
        self.pipeline = Pipeline([
            ("slice", DataSlicer(options.analysis.pt)),
            ("parametrize", InvariantMassExtractor(options.analysis.invmass)),
            ("fit", EpFitter(options.analysis.invmass.signal)),
            ("ranges", RangeEstimator(options.analysis.calibration)),
            ("data", DataExtractor(options.analysis.output)),
            ("ep", HistogramSelector("mass", plot)),
            ("fitf", FitfunctionAssigner(options.fitf, plot)),
        ])


def double_ratio(histograms, loggs, fitf, labels):
    for h, l in zip(histograms, labels):
        h.SetTitle(l)

    plot(
        histograms,
        logy=False,
        logx=False,
        xtitle="p_{T} (GeV/#it{c})",
        csize=(96, 128),
        oname="results/systematics/gescale/ep.pdf",
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
        logy=False,
        logx=False,
        ytitle="(E/p)_{Data} / (E/p)_{MC}",
        xtitle="p_{T} (GeV/#it{c})",
        csize=(96, 128),
        oname="results/systematics/gescale/double-ep.pdf",
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
            lambda x, loggs: double_ratio(x, loggs, options.data.fitf, labels)
        )
