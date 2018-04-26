#!/usr/bin/python

from transformer import TransformerBase
from options import EfficiencyOptions, MultirangeEfficiencyOptions
from .input import SingleHistInput
from analysis import Analysis
from pipeline import Pipeline, RatioUnion, HistogramSelector
from pipeline import ReducePipeline, ParallelPipeline, HistogramScaler

from broot import BROOT as br

# NB: This test is to compare different efficiencies
#     estimated from different productions
#


class EfficiencySimple(TransformerBase):

    def __init__(self, options, plot=False):
        super(EfficiencySimple, self).__init__(plot)
        self.pipeline = RatioUnion(
            Pipeline([
                ("ReconstructMesons", Analysis(options.analysis)),
                ("NumberOfMesons", HistogramSelector("npi0")),
                ("ScaleForAcceptance", HistogramScaler(options.scale))
            ]),
            SingleHistInput(options.genname)
        )


class EfficiencyMultirange(TransformerBase):

    def __init__(self, options, plot=False):
        super(EfficiencyMultirange, self).__init__(plot)

        self.pipeline = ReducePipeline(
            ParallelPipeline([
                ("efficiency-{0}".format(ranges), Efficiency(opt, plot))
                for (opt, ranges) in zip(options.suboptions,
                                         options.mergeranges)
            ]),
            lambda x: br.sum_trimm(x, options.mergeranges)
        )


class Efficiency(TransformerBase):

    _efficiency_types = {
        EfficiencyOptions: EfficiencySimple,
        MultirangeEfficiencyOptions: EfficiencyMultirange
    }

    def __init__(self, options=EfficiencyOptions(), plot=False):
        super(Efficiency, self).__init__(plot)
        EfficiencyType = self._efficiency_types.get(type(options))
        efficiency = EfficiencyType(options, plot)
        self.pipeline = efficiency.pipeline
