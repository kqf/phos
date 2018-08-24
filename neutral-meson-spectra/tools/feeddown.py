from spectrum.broot import BROOT as br
from spectrum.transformer import TransformerBase
from spectrum.pipeline import ComparePipeline, Pipeline, HistogramSelector
from spectrum.analysis import Analysis
from spectrum.comparator import Comparator


class ConfidenceLevelEstimator(TransformerBase):
    def __init__(self, fitf, plot=False):
        super(ConfidenceLevelEstimator, self).__init__(plot)
        self.fitf = fitf

    def transform(self, feeddown, loggs):
        errors = br.confidence_intervals(feeddown, self.fitf)
        title = "Feeddown correction approximation"
        title += "; p_{T}, GeV/c"
        title += "; #frac{dN(#pi^{0} #leftarrow K_{0}^{s})}{dp_{T}} / "
        title += "#frac{dN(all)}{dp_{T}}"
        feeddown.SetTitle(title)
        errors.SetTitle(title)
        errors.label = "approximation"
        errors.SetOption("e3")
        errors.SetFillStyle(3002)
        feeddown.logy = False
        Comparator(loggs=loggs, rrange=(-1, -1)).compare(feeddown, errors)
        return feeddown


class FeeddownEstimator(TransformerBase):
    def __init__(self, options, plot=False):
        super(FeeddownEstimator, self).__init__(plot)
        feeddown_main = ComparePipeline([
            ("feed-down",
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
