import ROOT
import numpy as np
import pandas as pd
from sklearn.pipeline import make_pipeline

import plotting
from trigger.trend import HistReader
from trigger.utils import style
ROOT.TH1.AddDirectory(False)
ROOT.gStyle.SetOptStat(0)


class RatioCalculator(object):
    def __init__(self, in_cols, out_col):
        super(RatioCalculator, self).__init__()
        self.in_cols = in_cols
        self.out_col = out_col

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X[self.out_col] = X[self.in_cols].apply(
            lambda x: self.ratio(*x), axis=1)
        return X

    def ratio(self, numerator, denominator):
        divided = numerator.Clone("{}_{}".format(
            numerator.GetName(),
            self.out_col))
        divided.Divide(numerator, denominator, 1, 1, "B")
        return divided


class RebinTransformer(object):
    _bins = np.array([0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8,
                      2.0, 2.2, 2.4, 2.6, 2.8, 3.0, 3.2, 3.4, 3.6, 3.8,
                      4.0, 4.2, 4.4, 4.6, 4.8, 5.0, 5.5, 6.0, 6.5, 7.0,
                      7.5, 8.0, 9.0, 10., 12., 14., 20., 30., 40.])

    def __init__(self, in_cols, out_col):
        super(RebinTransformer, self).__init__()
        self.in_cols = in_cols
        self.out_col = out_col

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X[self.out_col] = X[self.in_cols].apply(self.rebin)
        return X

    def rebin(self, hist):
        rebinned = hist.Rebin(len(self._bins) - 1, hist.GetName(), self._bins)
        rebinned.Sumw2()
        for i in range(1, len(self._bins)):
            delta = self._bins[i] - self._bins[i - 1]
            rebinned.SetBinContent(i, rebinned.GetBinContent(i) / delta)
        style(rebinned)
        return rebinned


def analyze_module(filepath, lst, nhists=8, pattern="TRU{}", sm=None):
    analysis = make_pipeline(
        HistReader("name", "all", filepath, "hPhotAllSM{}".format(sm), lst),
        RebinTransformer("all", "all_rebinned"),
        HistReader("name", "matched", filepath,
                   "hPhotTrigSM{}".format(sm), lst),
        RebinTransformer("matched", "matched_rebinned"),
        RatioCalculator(["matched_rebinned", "all_rebinned"], "turnon"),
    )
    outputs = pd.DataFrame(index=map(str, range(1, nhists + 1)))
    outputs["module_number"] = sm or outputs.index
    outputs["name"] = outputs.index.map(pattern.format)
    return analysis.fit_transform(outputs)


def turn_on_curves(filepath, lst="PHOSTriggerQAResultsL0", n_modules=4):
    for sm in range(1, n_modules + 1):
        plotter = plotting.Plotter()
        canvas = ROOT.TCanvas("TrendPlots", "TrendPlots", 1000, 500)
        output = analyze_module(filepath, lst, sm=sm)
        title = "Triggered clusters / All clusters in SM{}; E, GeV".format(sm)
        plotter.plot(output["turnon"], output["name"], canvas, title)
        plotting.save_canvas(canvas, "turn-on-curveu-sm-{}".format(sm))
        canvas.Update()
        raw_input()
