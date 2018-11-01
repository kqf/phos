import ROOT
from spectrum.processing import DataSlicer, InvariantMassExtractor
from spectrum.pipeline import Pipeline
from spectrum.pipeline import ComparePipeline
from spectrum.pipeline import TransformerBase
from spectrum.processing import RangeEstimator, DataExtractor
from spectrum.pipeline import HistogramSelector


class IdentityExtractor(object):
    def __init__(self, options):
        super(IdentityExtractor, self).__init__()
        self.options = options

    def transform(self, mass):
        mass.signal = mass.mass.Clone()

        formula = "gaus(0) + {}(3)".format(self.options.background)
        func = ROOT.TF1("func", formula, *self.options.fit_range)

        func.SetParNames(*self.options.par_names)
        func.SetParameter(0, 60)
        func.SetParameter(1, 1)
        func.SetParameter(2, 0.08)
        func.SetLineColor(ROOT.kRed + 1)
        mass.signal.Fit(func, "RQ")
        bkgrnd = ROOT.TF1("bkgrnd", self.options.background,
                          *self.options.fit_range)
        for i in range(3, func.GetNpar()):
            bkgrnd.SetParameter(i - 3, func.GetParameter(i))
        mass.sigf = func
        mass.bgrf = bkgrnd
        return mass


class EpFitter(object):

    def __init__(self, options):
        super(EpFitter, self).__init__()
        self.pipeline = [
            IdentityExtractor(options),
        ]

    def transform(self, masses, loggs):
        for estimator in self.pipeline:
            map(estimator.transform, masses)
        return masses


class EpRatioEstimator(TransformerBase):

    def __init__(self, options, plot=False):
        super(EpRatioEstimator, self).__init__(plot)
        self.pipeline = Pipeline([
            ("slice", DataSlicer(options.analysis.pt)),
            ("parametrize", InvariantMassExtractor(options.analysis.invmass)),
            ("fit", EpFitter(options.analysis.signalp)),
            ("ranges", RangeEstimator(options.analysis.spectrum)),
            ("data", DataExtractor(options.analysis.output)),
            ("ep", HistogramSelector("mass", plot))
        ])


class DataMCEpRatioEstimator(TransformerBase):
    def __init__(self, options, plot=False):
        super(DataMCEpRatioEstimator, self).__init__(plot)
        self.pipeline = ComparePipeline([
            ("data", EpRatioEstimator(options.data)),
            ("mc", EpRatioEstimator(options.mc)),
        ])
