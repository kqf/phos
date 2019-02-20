from __future__ import print_function

import ROOT
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import make_pipeline

import plotting
from utils import read_dataset
from utils import row_decoder
from utils import trendhist
from transformators import FunctionTransformer
# from utils import row_decoder
ROOT.TH1.AddDirectory(False)


class AcceptanceScaler(BaseEstimator, TransformerMixin):

    def __init__(self, in_cols, out_col):
        self.in_cols = in_cols
        self.out_col = out_col

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X[self.out_col] = X[self.in_cols].apply(
            lambda x: self.scale(*x), axis=1)
        return X

    @staticmethod
    def scale(hist, badmap):
        if not badmap:
            return hist
        bad_channels = badmap.GetEntries()
        all_channels = badmap.GetNbinsX() * badmap.GetNbinsY()

        scaled = hist.Clone("{}_acceptance".format(hist.GetName()))
        scaled.SetTitle("{} scaled for acceptance".format(hist.GetTitle()))
        scaled.Scale(1. / (all_channels - bad_channels))
        return scaled


class AverageCalculator(BaseEstimator, TransformerMixin):
    def __init__(self, in_col, out_col, info=None):
        self.in_col = in_col
        self.out_col = out_col
        self.info = info

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        average = self.average(X[self.in_col])
        payload = pd.DataFrame(
            [{
                self.out_col: average,
                "name": "average"
            }],
            index=["average"])
        return X.append(payload, sort=True)

    @staticmethod
    def average(hists):
        total = hists[0].Clone("average")
        total.Reset()
        for hist in hists:
            total.Add(hist)
        total.Scale(1. / len(hists))
        return total


class EventsScaler(BaseEstimator, TransformerMixin):
    def __init__(self, in_col, out_col, raw_col, eventmap):
        super(EventsScaler, self).__init__(raw_col, out_col)
        self.input = in_col
        self.out_col = out_col
        self.eventmap = eventmap
        self._eventmap_cleaned = None

    def fit(self, X, y=None):
        super(EventsScaler, self).fit(X, y)
        return self

    def transform(self, X):
        X[self.out_col] = X[self.input].apply(self.scale)
        return X

    def scale(self, hist):
        divided = hist.Clone("{}_{}".format(hist.GetName(), self.out_col))
        divided.Divide(hist, self._eventmap_cleaned, 1, 1, "B")
        divided.LabelsOption("v")
        return divided


def agg_hists(x):
    d = {}
    d["nruns"] = len(x["run"])
    d["matched"] = trendhist(x["run"], x["matched"])
    d["all"] = trendhist(x["run"], x["all"])
    return pd.Series(d, index=["nruns", "matched", "all"])


def process(filepath, badmap_fname):
    df = read_dataset(filepath, rules=row_decoder)
    query = make_pipeline(
        FunctionTransformer("hPhotAll", "all", lambda x: x.GetEntries()),
        FunctionTransformer("hPhotTrig", "matched", lambda x: x.GetEntries())
        # AcceptanceScaler(["cleaned", "badmap"], "acceptance"),
        # EventsScaler("acceptance", "scaled",
        #              raw_col="raw", eventmap=event_runs),
        # AverageCalculator("scaled", "scaled")
    )

    return query.fit_transform(df).groupby(["module", "tru"]).apply(agg_hists)


def fired_trigger_fraction(mtriggers, triggers):
    output = []
    for trig, mtrig in zip(triggers, mtriggers):
        fired = mtrig.Clone()
        fired.Divide(mtrig, trig, 1, 1, "B")
        title = "Ratio of matched trigger clusters to all triggered clusters"
        fired.SetTitle(title)
        output.append(fired)
    return output


def trend(filepath, lst="PHOSTriggerQAResultsL0",
          badmap_fname="../BadMap_LHC16-updated.root"):
    plotter = plotting.Plotter()
    canvas = ROOT.TCanvas("TrendPlots", "TrendPlots", 1000, 500)
    canvas.Divide(1, 3)

    triggers = process("hRunTriggers", lst, filepath, badmap_fname)
    title = "Number of 4x4 patches per run"
    title += ";; # patches / accepntace/ #events"
    plotter.plot(triggers["scaled"],
                 triggers["name"],
                 canvas.cd(1),
                 title)

    mtriggers = process("hRunMatchedTriggers", lst, filepath, badmap_fname)
    title = "Numbero of matched 4x4 patches per run"
    title += ";;# patches / accepntace/ #events"
    plotter.plot(mtriggers["scaled"],
                 mtriggers["name"],
                 canvas.cd(2),
                 title)

    fired_fraction = fired_trigger_fraction(mtriggers["scaled"],
                                            triggers["scaled"])

    title = "Number of matched tirggers / number of all triggers"
    title += ";;#patches / # matched"
    plotter.plot(fired_fraction,
                 triggers["name"],
                 canvas.cd(3),
                 title)

    plotting.save_canvas(canvas, "trending")
    canvas.Update()
    raw_input()


def trend_tru(filepath, badmap_fname="../BadMap_LHC16-updated.root",
              n_modules=4):
    histograms = process(filepath, badmap_fname=badmap_fname)
    histograms.reset_index(inplace=True)
    for sm in range(1, n_modules + 1):
        current_module = "SM{}".format(sm)
        sm_hists = histograms[histograms["module"] == current_module]
        canvas = ROOT.TCanvas("TrendPlots", "TrendPlots", 1000, 500)
        canvas.Divide(1, 3)

        title = "Number of 4x4 patches per run SM{}".format(sm)
        title += ";; # patches / accepntace/ #events"
        plotter = plotting.Plotter()
        plotter.plot(sm_hists["matched"],
                     sm_hists["tru"],
                     canvas.cd(1),
                     title, runwise=True)

        title = "Numbero of matched 4x4 patches per run SM{}".format(sm)
        title += ";;# patches / accepntace/ #events"
        plotter.plot(sm_hists["all"],
                     sm_hists["tru"],
                     canvas.cd(2),
                     title, runwise=True)
        fired_fraction = fired_trigger_fraction(sm_hists["matched"],
                                                sm_hists["all"])

        title = "Number of matched tirggers"
        title += " / number of all triggers SM{}".format(sm)
        title += ";;#patches / # matched"
        plotter.plot(fired_fraction,
                     sm_hists["tru"],
                     canvas.cd(3),
                     title)

        plotting.save_canvas(canvas, "trending-tru-sm-{}".format(sm))
        canvas.Update()
        raw_input()

    # for sm in range(1, n_modules + 1):
    #     plotter = plotting.Plotter()
    #     canvas = ROOT.TCanvas("TrendPlots", "TrendPlots", 1000, 500)
    #     canvas.Divide(1, 3)

    #     triggers = process("hRunTriggersSM{}".format(sm),
    #                        lst, filepath, badmap_fname,
    #                        pattern="TRU{}", nhists=8, sm=sm)
    #     title = "Number of 4x4 patches per run SM{}".format(sm)
    #     title += ";; # patches / accepntace/ #events"
    #     plotter.plot(triggers["scaled"],
    #                  triggers["name"],
    #                  canvas.cd(1),
    #                  title)

    #     mtriggers = process("hRunMatchedTriggersSM{}".format(sm),
    #                         lst, filepath, badmap_fname,
    #                         pattern="TRU{}", nhists=8, sm=sm)
    #     title = "Numbero of matched 4x4 patches per run SM{}".format(sm)
    #     title += ";;# patches / accepntace/ #events"
    #     plotter.plot(mtriggers["scaled"],
    #                  mtriggers["name"],
    #                  canvas.cd(2),
    #                  title)

    #     fired_fraction = fired_trigger_fraction(mtriggers["scaled"],
    #                                             triggers["scaled"])

    #     title = "Number of matched tirggers"
    #     title += " / number of all triggers SM{}".format(sm)
    #     title += ";;#patches / # matched"
    #     plotter.plot(fired_fraction,
    #                  triggers["name"],
    #                  canvas.cd(3),
    #                  title)

    #     plotting.save_canvas(canvas, "trending-tru-sm-{}".format(sm))
    #     canvas.Update()
    #     raw_input()
