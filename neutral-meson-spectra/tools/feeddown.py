import numpy as np

from spectrum.broot import BROOT as br
from spectrum.pipeline import TransformerBase
from spectrum.pipeline import ComparePipeline, Pipeline, HistogramSelector
from spectrum.analysis import Analysis
from spectrum.comparator import Comparator
from spectrum.outputcreator import output_histogram
from vault.datavault import DataVault


def data_feeddown():
    return (
        DataVault().input(
            "pythia8",
            listname="FeeddownSelection",
            use_mixing=False,
            histname="MassPt_#pi^{0}_feeddown_K^{s}_{0}",
            prefix=""
        ),
        DataVault().input("pythia8", listname="FeeddownSelection"),
    )


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
        corr = br.copy(feeddown)
        corr.Reset()
        for b in br.range(feeddown):
            corr.SetBinContent(b, 1. - self.fitf.Eval(corr.GetBinCenter(b)))
        # NB: I don't know why It should be scaled by 1.
        #     otherwise it plots something strange
        corr.Scale(1.0)
        return corr


class FeeddownEstimator(TransformerBase):
    def __init__(self, options, plot=False):
        super(FeeddownEstimator, self).__init__(plot)
        self.pt = options.regular.pt.ptedges
        self.particle = options.particle
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

    def transform(self, data, loggs):
        if data and self.particle != "#pi^{0}":
            raise IOError(
                "Found nonempty input for feeddown estimator "
                "for particle {}. "
                "Only pions have sufficient statistics".format(self.particle)
            )

        if self.particle != "#pi^{0}":
            data = zip(np.ones(len(self.pt) - 1), np.zeros(len(self.pt) - 1))
            return output_histogram(
                (min(self.pt), max(self.pt)),
                "feeddown",
                "No Feeddown",
                "feeddown",
                self.pt,
                data
            )

        return super(FeeddownEstimator, self).transform(data, loggs)
