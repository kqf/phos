import array
import ROOT

import spectrum.broot as br
from spectrum.pipeline import TransformerBase
from spectrum.pipeline import ComparePipeline, Pipeline, HistogramSelector
from spectrum.pipeline import FunctionTransformer
from spectrum.analysis import Analysis
from spectrum.vault import DataVault


def data_feeddown(dummy=False):
    if dummy:
        return None

    return (
        DataVault().input(
            "pythia8",
            listname="FeeddownSelection",
            histname="hMassPt_#pi^{0}_feeddown_K^{s}_{0}",
            prefix="",
            suffixes=None,
        ),
        DataVault().input("pythia8", listname="FeeddownSelection"),
    )


class CorrectionEstimator(TransformerBase):
    def __init__(self, fitf, pt, plot=False):
        super(CorrectionEstimator, self).__init__(plot)
        self.fitf = fitf
        self.pt = array.array('f', pt)

    def transform(self, feeddown, loggs):
        title = "MC; p_{T} (GeV/#it{c})"
        title += "; #frac{dN(#pi^{0} #leftarrow K_{0}^{s})}{dp_{T}} / "
        title += "#frac{dN(all)}{dp_{T}}"
        feeddown.Fit(self.fitf, "QR")
        corr = ROOT.TH1F("feeddown", "Feed-down", len(self.pt) - 1, self.pt)
        for b in br.hrange(corr):
            corr.SetBinContent(b, 1. - self.fitf.Eval(corr.GetBinCenter(b)))
            corr.SetBinError(b, 0)
        return corr


class FeeddownEstimator(TransformerBase):
    def __init__(self, options, plot=False):
        super(FeeddownEstimator, self).__init__(plot)
        self.pt = array.array('f', options.pt)
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
            ("plot", FunctionTransformer(options.plot_func)),
            ("feeddown_fit", CorrectionEstimator(options.fitf, self.pt, plot))
        ])

    def transform(self, data, loggs):
        if data and self.particle != "#pi^{0}":
            raise IOError(
                "Found nonempty input for feeddown estimator "
                "for particle {}. "
                "Only pions have sufficient statistics".format(self.particle)
            )

        if self.particle != "#pi^{0}":
            return br.unity(
                ROOT.TH1F("feeddown", "Feed-down", len(self.pt) - 1, self.pt)
            )

        return super(FeeddownEstimator, self).transform(data, loggs)
