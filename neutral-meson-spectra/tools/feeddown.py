from spectrum.broot import BROOT as br
from spectrum.transformer import TransformerBase
from spectrum.pipeline import ComparePipeline, Pipeline, HistogramSelector
from spectrum.analysis import Analysis


class ConfidenceLevelEstimator(TransformerBase):
    def __init__(self, fitf, plot=False):
        super(ConfidenceLevelEstimator, self).__init__(plot)
        self.fitf = fitf

    def transform(self, feeddown, loggs):
        return feeddown, br.confidence_intervals(feeddown, self.fitf)


class FeeddownEstimator(TransformerBase):
    def __init__(self, options, plot=False):
        super(FeeddownEstimator, self).__init__(plot)
        feeddown_main = ComparePipeline([
            ("feeddown",
                Pipeline([
                    ("analysis", Analysis(options.feeddown, plot)),
                    ("nmesons", HistogramSelector("nmesons"))
                ])
             ),
            ("regular",
                Pipeline([
                    ("analysis", Analysis(options.regular, plot)),
                    ("nmesons", HistogramSelector("nmesons"))
                ])
             ),
        ], plot)

        self.pipeline = Pipeline([
            ("feeddown_extraction", feeddown_main),
            ("feeddown_fit", ConfidenceLevelEstimator(options.fitf, plot))
        ])
