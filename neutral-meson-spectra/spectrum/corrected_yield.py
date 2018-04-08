from broot import BROOT as br
from spectrum import Spectrum
from analysis import Analysis
from .input import Input
from options import CorrectedYieldOptions
from efficiency import Efficiency, EfficiencyMultirange
from comparator import Comparator
from transformer import TransformerBase
from pipeline import ReducePipeline, ParallelPipeline, Pipeline, HistogramSelector

class CorrectedYield(TransformerBase):
    def __init__(self, options=CorrectedYieldOptions(), plot=False):
        super(CorrectedYield, self).__init__(plot)
        efficiency = Efficiency if options.issimple else EfficiencyMultirange
        self.pipeline = ReducePipeline(
            ParallelPipeline([
                ('raw-yield',
                    Pipeline([
                        ('analysis', Analysis(options.analysis, plot)),
                        ('spectrum', HistogramSelector(options.spectrum))
                    ])
                ),
                ('efficiency', efficiency(options.efficiency, plot))
            ]),
            Comparator().compare
        )