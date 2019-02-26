from __future__ import print_function

import ROOT
import pandas as pd
from sklearn.pipeline import make_pipeline
from sklearn.base import BaseEstimator, TransformerMixin

import plotting
from utils import read_dataset
from utils import row_decoder_sm
from utils import row_decoder_tru
from utils import trendhist
from transformators import FunctionTransformer
from transformators import RatioCalculator
ROOT.TH1.AddDirectory(False)


class BadMapCalculator(BaseEstimator, TransformerMixin):
    def __init__(self, in_col, out_col,
                 filepath, pattern, listpath=None):
        self.in_col = in_col
        self.out_col = out_col
        self.filepath = filepath
        self.pattern = pattern
        self.listpath = listpath

    def fit(self, X, y=None):
        modules = X[self.in_col].unique()
        infile = ROOT.TFile(self.filepath)

        hists = {
            mod_name:
            infile.Get("{}{}".format(self.pattern, mod_name[-1]))
            for mod_name in modules
        }

        self.mapping_ = {
            mod_name:
                h.GetNbinsX() * h.GetNbinsY() - h.GetEntries()
                for mod_name, h in hists.iteritems()
        }
        return self

    def transform(self, X):
        print(self.mapping_)
        X[self.out_col] = X[self.in_col].map(self.mapping_)
        return X


def agg_hists(x):
    d = {}
    d["nruns"] = len(x["run"])
    d["matched"] = trendhist(x["run"], x["matched"])
    d["all"] = trendhist(x["run"], x["all"])
    d["events"] = trendhist(x["run"], x["events"])
    d["acceptance"] = trendhist(x["run"], x["acceptance"])
    return pd.Series(d, index=["nruns", "matched", "all",
                               "acceptance", "events"])


def process(filepath, badmap_fname, rules):
    df = read_dataset(filepath, rules=rules)
    query = make_pipeline(
        FunctionTransformer("hPhotAll", "all", lambda x: x.GetEntries()),
        FunctionTransformer("hPhotTrig", "matched", lambda x: x.GetEntries()),
        BadMapCalculator("module", "acceptance",
                         filepath=badmap_fname,
                         pattern="PHOS_BadMap_mod",
                         ),
    )

    return query.fit_transform(df)


def postprocess(df):
    query = make_pipeline(
        RatioCalculator(["all", "acceptance"], "all"),
        RatioCalculator(["all", "events"], "all"),
        RatioCalculator(["matched", "acceptance"], "matched"),
        RatioCalculator(["matched", "events"], "matched"),
        RatioCalculator(["matched", "all"], "matched_all"),
    )

    return query.fit_transform(df)


def trend(filepath, badmap_fname="../BadMap_LHC16-updated.root", n_modules=4):
    histograms = process(filepath, badmap_fname=badmap_fname,
                         rules=row_decoder_sm)

    groupped = histograms.groupby(["module"]).apply(agg_hists)
    groupped.reset_index(inplace=True)
    groupped = postprocess(groupped)

    canvas = ROOT.TCanvas("TrendPlots", "TrendPlots", 1000, 500)
    canvas.Divide(1, 3)

    title = "Number of 4x4 patches per run"
    title += ";; # patches / accepntace / #events"
    plotter = plotting.Plotter()
    plotter.plot(groupped["all"],
                 groupped["module"],
                 canvas.cd(1),
                 title, runwise=True)

    title = "Numbero of matched 4x4 patches per run"
    title += ";;# patches / accepntace / #events"
    plotter.plot(groupped["matched"],
                 groupped["module"],
                 canvas.cd(2),
                 title, runwise=True)

    title = "Number of matched tirggers"
    title += " / number of all triggers"
    title += ";;#patches / # matched"
    plotter.plot(groupped["matched_all"],
                 groupped["module"],
                 canvas.cd(3),
                 title)

    plotting.save_canvas(canvas, "trending-sm")
    canvas.Update()
    raw_input()


def trend_tru(filepath, badmap_fname="../BadMap_LHC16-updated.root",
              n_modules=4):
    histograms = process(filepath, badmap_fname=badmap_fname,
                         rules=row_decoder_tru)

    groupped = histograms.groupby(["module", "tru"]).apply(agg_hists)
    groupped.reset_index(inplace=True)
    groupped = postprocess(groupped)
    for sm in range(1, n_modules + 1):
        current_module = "SM{}".format(sm)
        sm_hists = groupped[groupped["module"] == current_module]
        canvas = ROOT.TCanvas("TrendPlots", "TrendPlots", 1000, 500)
        canvas.Divide(1, 3)

        title = "Number of 4x4 patches per run SM{}".format(sm)
        title += ";; # patches / accepntace / #events"
        plotter = plotting.Plotter()
        plotter.plot(sm_hists["all"],
                     sm_hists["tru"],
                     canvas.cd(1),
                     title, runwise=True)

        title = "Numbero of matched 4x4 patches per run SM{}".format(sm)
        title += ";;# patches / accepntace / #events"
        plotter.plot(sm_hists["matched"],
                     sm_hists["tru"],
                     canvas.cd(2),
                     title, runwise=True)

        title = "Number of matched tirggers"
        title += " / number of all triggers SM{}".format(sm)
        title += ";;#patches / # matched"
        plotter.plot(sm_hists["matched_all"],
                     sm_hists["tru"],
                     canvas.cd(3),
                     title)

        plotting.save_canvas(canvas, "trending-tru-sm-{}".format(sm))
        canvas.Update()
        raw_input()
