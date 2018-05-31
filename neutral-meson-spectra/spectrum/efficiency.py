#!/usr/bin/python

from transformer import TransformerBase
from options import EfficiencyOptions, CompositeEfficiencyOptions
from .input import SingleHistInput
from analysis import Analysis
from pipeline import Pipeline, RatioUnion, HistogramSelector
from pipeline import OutputDecorator
from pipeline import ReducePipeline, ParallelPipeline, HistogramScaler
from broot import BROOT as br

# NB: This test is to compare different efficiencies
#     estimated from different productions
#


class SimpleEfficiency(TransformerBase):

    def __init__(self, options, plot=False):
        super(SimpleEfficiency, self).__init__(plot)
        efficiency = RatioUnion(
            Pipeline([
                ("ReconstructMesons", Analysis(options.analysis)),
                ("NumberOfMesons", HistogramSelector("nmesons")),
                ("ScaleForAcceptance", HistogramScaler(options.scale))
            ]),
            SingleHistInput(options.genname)
        )
        self.pipeline = Pipeline([
            ('efficiency', efficiency),
            ('decorate', OutputDecorator(*options.decorate))
        ])


class CompositeEfficiency(TransformerBase):

    def __init__(self, options, plot=False):
        super(CompositeEfficiency, self).__init__(plot)

        self.pipeline = ReducePipeline(
            ParallelPipeline([
                (self._stepname(ranges), Efficiency(opt, plot))
                for (opt, ranges) in zip(options.suboptions,
                                         options.mergeranges)
            ]),
            lambda x: br.sum_trimm(x, options.mergeranges)
        )

    def _stepname(self, ranges):
        return "#varepsilon {0} < p_{T} < {1} GeV/c".format(*ranges, T='{T}')


class Efficiency(TransformerBase):

    _efficiency_types = {
        EfficiencyOptions: SimpleEfficiency,
        CompositeEfficiencyOptions: CompositeEfficiency
    }

    def __init__(self, options=EfficiencyOptions(), plot=False):
        super(Efficiency, self).__init__(plot)
        EfficiencyType = self._efficiency_types.get(type(options))
        efficiency = EfficiencyType(options, plot)
        self.pipeline = efficiency.pipeline
