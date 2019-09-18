import ROOT

from spectrum.analysis import Analysis
from spectrum.pipeline import TransformerBase
from spectrum.options import Options
from spectrum.pipeline import Pipeline, HistogramSelector
from spectrum.pipeline import FitfunctionAssigner
from spectrum.pipeline import ComparePipeline
from spectrum.pipeline import OutputDecorator
from spectrum.tools.unityfit import unityfit
from vault.datavault import DataVault


def tof_data():
    return (
        DataVault().input("data", histname="MassPtSM0"),
        DataVault().input("data", "isolated", histname="MassPtSM0"),
    )


def tof_data_stable():
    return (
        DataVault().input("data", "stable"),
        DataVault().input("data", "isolated", histname="MassPtSM0"),
    )


class TofUncertaintyOptions(object):

    def __init__(self):
        super(TofUncertaintyOptions, self).__init__()
        self.data = Options()
        self.isolated = Options()
        self.decorate = self.data.particle, "isolated"
        self.fit_range = 1.0, 7.5
        self.fitf = ROOT.TF1("ratio", "1. - pol0(0)", *self.fit_range)
        self.fitf.SetParameter(0, 0.02)


class RatioFitter(TransformerBase):
    title = "TOF uncertainty; p_T, GeV/c; Relateive error, %"

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
        ratio = ComparePipeline([
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
        ], plot)

        self.pipeline = Pipeline([
            ("spectrum_isolated_spectra_ratio", ratio),
            ("pol0_fit", RatioFitter(options.fit_range))
        ])
