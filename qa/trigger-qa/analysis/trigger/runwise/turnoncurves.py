import ROOT
import pandas as pd
from sklearn.pipeline import make_pipeline
from trigger.transformators import RatioCalculator
from trigger.transformators import RebinTransformer
from trigger.transformators import FunctionTransformer
from trigger.utils import trendhist
from trigger.utils import row_decoder
from trigger.utils import read_dataset
from trigger.plotting import Plotter, save_canvas


def integrate(hist, trigger_threshold=4):
    return hist.Integral(hist.FindBin(trigger_threshold), hist.GetNbinsX())


def turnon_level(hist, trigger_threshold=4, trigger_max=50):
    func = ROOT.TF1("func", "pol0", trigger_threshold, trigger_max)
    func.SetParameter(0, 1)
    func.SetParLimits(0, 0, 1.02)
    # hist.GetXaxis().SetRangeUser(trigger_threshold, trigger_max)
    hist.Fit(func, "qRL")
    # hist.Draw()
    # ROOT.gPad.Update()
    # raw_input()
    # print func.GetParameter(0)
    # assert False
    return func.GetParameter(0)


def report(x):
    d = {}
    d["nruns"] = len(x["run"])
    d["integral_hist"] = trendhist(x["run"], x["integral"])
    d["efficiency_hist"] = trendhist(x["run"], x["efficiency"])
    return pd.Series(d, index=["nruns", "integral_hist", "efficiency_hist"])


def runwise_histograms(filepath):
    df = read_dataset(filepath, rules=row_decoder)
    analysis = make_pipeline(
        RebinTransformer("hPhotAll", "all_rebinned"),
        RebinTransformer("hPhotTrig", "matched_rebinned"),
        RatioCalculator(["matched_rebinned", "all_rebinned"], "turnon"),
        FunctionTransformer("turnon", "integral", integrate),
        FunctionTransformer("turnon", "efficiency", turnon_level)
    )
    return analysis.fit_transform(df).groupby(["module", "tru"]).apply(report)


def turnon_stats(filepath, n_modules=4):
    histograms = runwise_histograms(filepath)
    histograms.reset_index(inplace=True)
    for sm in range(1, n_modules + 1):
        current_module = "SM{}".format(sm)
        sm_hists = histograms[histograms["module"] == current_module]
        canvas = ROOT.TCanvas("TrendPlots", "TrendPlots", 1000, 500)
        canvas.Divide(1, 2)

        title = "Turn-on curve fitted above the 4 GeV/c, SM{}".format(sm)
        title += ";; efficiency"
        plotter = Plotter()
        plotter.plot(sm_hists["efficiency_hist"],
                     sm_hists["tru"],
                     canvas.cd(1),
                     title, runwise=True)

        title = "Area under turnon curve above 4 GeV/c, SM{}".format(sm)
        title += ";; integral"
        plotter.plot(sm_hists["integral_hist"],
                     sm_hists["tru"],
                     canvas.cd(2),
                     title, runwise=True)

        save_canvas(canvas, "trending-turnon-tru-sm-{}".format(sm))
        canvas.Update()
        raw_input()
