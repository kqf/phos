import ROOT

from spectrum.analysis import Analysis
from spectrum.transformer import TransformerBase
from spectrum.options import Options
from spectrum.pipeline import Pipeline, HistogramSelector
from spectrum.pipeline import FitfunctionAssigner
from spectrum.pipeline import ComparePipeline
from spectrum.pipeline import OutputDecorator
from tools.unityfit import unityfit


class TofUncertaintyOptions(object):

    def __init__(self):
        super(TofUncertaintyOptions, self).__init__()
        self.data = Options()
        self.isolated = Options()
        self.decorate = self.data.particle, "isolated"
        self.fit_range = 1.0, 10
        self.fitf = ROOT.TF1("ratio", "1. - pol0(0)", *self.fit_range)


class RatioFitter(TransformerBase):
    def __init__(self, fit_range, plot=False):
        super(RatioFitter, self).__init__(plot)
        self.fit_range = fit_range

    def transform(self, ratio, loggs):
        return unityfit(
            ratio,
            "tof_uncertainty",
            "TOF uncertainty; p_T, GeV/c; Relateive error, %",
            self.fit_range
        )


class TofUncertainty(TransformerBase):

    def __init__(self, options, plot=False):
        super(TofUncertainty, self).__init__(plot)
        ratio = ComparePipeline([
            ('25ns', Pipeline([
                ("reconstruction", Analysis(options.data, plot)),
                ("spectrum", HistogramSelector("spectrum", plot)),
                ("FitF", FitfunctionAssigner(options.fitf, plot)),
            ])),
            ('isolated', Pipeline([
                ("ReconstructMesons", Analysis(options.isolated, plot)),
                ("spectrum", HistogramSelector("spectrum", plot)),
                ("decorate", OutputDecorator(*options.decorate)),
            ])),
        ], True)

        self.pipeline = Pipeline([
            ("spectrum_isolated_spectra_ratio", ratio),
            ("pol0_fit", RatioFitter(options.fit_range))
        ])
