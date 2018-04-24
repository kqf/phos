from analysis import Analysis
from options import CorrectedYieldOptions
from efficiency import Efficiency
from comparator import Comparator
from transformer import TransformerBase
from pipeline import ReducePipeline, ParallelPipeline
from pipeline import Pipeline, HistogramSelector


class CorrectedYield(TransformerBase):
    def __init__(self, options=CorrectedYieldOptions(), plot=False):
        super(CorrectedYield, self).__init__(plot)
        self.pipeline = ReducePipeline(
            ParallelPipeline([
                ('raw-yield',
                    Pipeline([
                        ('analysis', Analysis(options.analysis, plot)),
                        ('spectrum', HistogramSelector(options.spectrum))
                    ])
                 ),
                ('efficiency', Efficiency(options.efficiency, plot))
            ]),
            Comparator().compare
        )


class YieldRatio(TransformerBase):
    def __init__(self, options_eta, options_pi0, plot=False):
        super(YieldRatio, self).__init__(plot)
        self.pipeline = ReducePipeline(
            ParallelPipeline([
                ('#eta', CorrectedYield(options_eta, plot)),
                ('#pi^{0}', CorrectedYield(options_pi0, plot)),
            ]),
            Comparator().compare
        )
