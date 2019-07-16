from math import pi
from analysis import Analysis
from options import CorrectedYieldOptions
from efficiency import Efficiency
from pipeline import TransformerBase
from pipeline import Pipeline, HistogramSelector, OutputDecorator
from pipeline import ParallelPipeline, ReducePipeline
from pipeline import ComparePipeline
from pipeline import OutputFitter
from pipeline import HistogramScaler
from tools.feeddown import FeeddownEstimator
from broot import BROOT as br


class InvariantYield(TransformerBase):
    def transform(self, hist, loggs):
        normalized = br.divide_by_bin_centers(hist)
        normalized.Scale(1. / 2 / pi)
        normalized.logy = True
        normalized.logx = True
        return normalized


class CorrectedYield(TransformerBase):
    def __init__(self, options=CorrectedYieldOptions(), plot=False):
        super(CorrectedYield, self).__init__(plot)
        raw_yield = Pipeline([
            ("analysis", Analysis(options.analysis, plot)),
            ("spectrum", HistogramSelector(options.spectrum))
        ])

        fyield = ReducePipeline(
            ParallelPipeline([
                ("raw_yield", raw_yield),
                ("feed-down", FeeddownEstimator(options.feeddown))
            ]),
            self.multiply)

        compare = ComparePipeline([
            ("yield", fyield),
            ("efficiency", Efficiency(options.efficiency, plot))
        ], plot)

        self.pipeline = Pipeline([
            ("corrected yield", compare),
            ("normalization", HistogramScaler(
                options.normalization / options.branching_ratio)),
            ("fix naming", OutputDecorator(options.analysis.particle)),
            ("invariant yield", InvariantYield()),
            ("fitted yield", OutputFitter(options)),
            ("decorate output", OutputDecorator(**options.decorate)),
        ])

    def multiply(self, calculations, loggs):
        ryield, feeddown = calculations
        cyield = ryield.Clone(ryield.GetName() + "_corrected_yield")
        cyield.Multiply(feeddown)
        loggs.update({"reduced_output": cyield})
        return cyield


class YieldRatio(TransformerBase):
    def __init__(self, options_eta, options_pi0, plot=False):
        super(YieldRatio, self).__init__(plot)
        self.pipeline = ComparePipeline([
            ("#eta", CorrectedYield(options_eta, plot)),
            ("#pi^{0}", CorrectedYield(options_pi0, plot)),
        ], plot)
