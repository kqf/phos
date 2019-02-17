import ROOT
import pandas as pd
from sklearn.pipeline import make_pipeline
from transformators import RatioCalculator, RebinTransformer

import plotting
from trigger.trend import HistReader
ROOT.TH1.AddDirectory(False)
ROOT.gStyle.SetOptStat(0)


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
        plotting.save_canvas(canvas, "turn-on-curve-sm-{}".format(sm))
        canvas.Update()
        raw_input()
