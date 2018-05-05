from analysis import Analysis
from options import CorrectedYieldOptions
from efficiency import Efficiency
from transformer import TransformerBase
from pipeline import Pipeline, HistogramSelector
from pipeline import ComparePipeline
from pipeline import OutputFitter


class CorrectedYield(TransformerBase):
    def __init__(self, options=CorrectedYieldOptions(), plot=False):
        super(CorrectedYield, self).__init__(plot)
        compare = ComparePipeline([
            ('raw yield', Pipeline([
                ('analysis', Analysis(options.analysis, plot)),
                ('spectrum', HistogramSelector(options.spectrum))
            ])),
            ('efficiency', Efficiency(options.efficiency, plot))
        ], plot)

        self.pipeline = Pipeline([
            ('corrected yield', compare),
            ('fitted yield', OutputFitter(options)),
        ])


class YieldRatio(TransformerBase):
    def __init__(self, options_eta, options_pi0, plot=False):
        super(YieldRatio, self).__init__(plot)
        self.pipeline = ComparePipeline([
            ('#eta', CorrectedYield(options_eta, plot)),
            ('#pi^{0}', CorrectedYield(options_pi0, plot)),
        ], plot)
