from math import pi

from spectrum.analysis import Analysis
from spectrum.options import CorrectedYieldOptions
from spectrum.efficiency import Efficiency
from spectrum.efficiency import simple_efficiency_data, efficiency_data
from spectrum.pipeline import TransformerBase
from spectrum.pipeline import Pipeline, HistogramSelector, OutputDecorator
from spectrum.pipeline import ParallelPipeline, ReducePipeline
from spectrum.pipeline import ComparePipeline
from spectrum.pipeline import HistogramScaler

import spectrum.broot as br

from spectrum.tools.feeddown import FeeddownEstimator
from spectrum.tools.feeddown import data_feeddown
from spectrum.vault import DataVault


def simple_cyield_data(particle):
    needs_dummy_feeddown = particle == "#eta"
    return (
        (
            DataVault().input("data", histname="MassPtSM0"),
            data_feeddown(dummy=needs_dummy_feeddown),
        ),
        simple_efficiency_data(particle=particle)
    )


def cyield_data(particle, listname_eff="PhysEff"):
    needs_dummy_feeddown = particle == "#eta"
    return (
        (
            DataVault().input("data", histname="MassPtSM0"),
            data_feeddown(dummy=needs_dummy_feeddown),
        ),
        efficiency_data(particle=particle, listname=listname_eff)
    )


class InvariantYield(TransformerBase):
    _ytitle = "#frac{1}{2 #pi #it{p}_{T}}"

    def transform(self, hist, loggs):
        normalized = br.divide_by_bin_centers(hist)
        normalized.Scale(1. / 2 / pi)
        normalized.logy = True
        normalized.logx = True
        self._update_ytitle(normalized)
        return normalized

    @classmethod
    def _update_ytitle(cls, hist):
        title = "{}{}".format(cls._ytitle, hist.GetYaxis().GetTitle().strip())
        hist.GetYaxis().SetTitle(title)
        hist.SetTitle("Invariant yields for LHC16 data")
        return hist


class CorrectedYield(TransformerBase):
    def __init__(self, options=CorrectedYieldOptions(), plot=False):
        super(CorrectedYield, self).__init__(plot)
        raw_yield = Pipeline([
            ("analysis", Analysis(options.analysis, plot)),
            ("spectrum", HistogramSelector(options.spectrum))
        ])

        fyield = ReducePipeline(
            ParallelPipeline([
                ("raw yield", raw_yield),
                ("feed down", FeeddownEstimator(options.feeddown))
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
            ("decorate output", OutputDecorator(**options.decorate)),
            ("invariant yield", InvariantYield()),
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
            ("#eta", CorrectedYield(options_eta)),
            ("#pi^{0}", CorrectedYield(options_pi0)),
        ], plot)
