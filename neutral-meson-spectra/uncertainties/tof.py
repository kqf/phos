import ROOT

from spectrum.analysis import Analysis
from spectrum.transformer import TransformerBase
from spectrum.options import Options
from spectrum.pipeline import Pipeline, HistogramSelector
from spectrum.pipeline import FitfunctionAssigner
from spectrum.pipeline import ComparePipeline
from spectrum.pipeline import OutputDecorator
from spectrum.broot import BROOT as br
from spectrum.comparator import Comparator


class TofUncertaintyOptions(object):

    def __init__(self):
        super(TofUncertaintyOptions, self).__init__()
        self.data = Options()
        self.isolated = Options()
        # NB: Don"t assingn to get an exception
        self.fitf = None
        self.decorate = self.data.particle, "isolated"
        self.fit_range = 1.0, 10


class RatioFitter(TransformerBase):
    def __init__(self, fit_range, plot=False):
        super(RatioFitter, self).__init__(plot)
        self.fit_range = fit_range

    def transform(self, ratio, loggs):
        fitf = ROOT.TF1("ratio", "1. - pol0(0)", *self.fit_range)
        fitf.SetParameter(0, 0.0)
        ratio.Fit(fitf, "R")
        # Comparator().compare(ratio)

        sys_error = abs(fitf.GetParameter(0))
        sys_error_conf = fitf.GetParError(0)

        output = ratio.Clone("tof_uncertainty")
        output.Reset()
        output.SetTitle("TOF uncertainty; p_T, GeV/c; Relateive error, %")
        for i in br.range(output):
            output.SetBinContent(i, sys_error)
            output.SetBinError(i, sys_error_conf)
        return output


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
