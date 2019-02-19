import ROOT
import pandas as pd
from sklearn.pipeline import make_pipeline
from trigger.transformators import RatioCalculator
from trigger.transformators import RebinTransformer
from trigger.transformators import FunctionTransformer
from trigger.utils import trendhist
from trigger.plotting import Plotter, save_canvas


def row_decoder(listkey, sm_start=1, sm_stop=4, tru_start=1, tru_stop=8):
    lst, output = listkey.ReadObj(), []

    for sm in range(sm_start, sm_stop + 1):
        for tru in range(tru_start, tru_stop + 1):
            output.append({
                "run": int(listkey.GetName()),
                "module": "SM{}".format(sm),
                "tru": "TRU{}".format(tru),
                "hPhotAll": lst.FindObject(
                    "hPhotAllSM{}TRU{}".format(sm, tru)),
                "hPhotTrig": lst.FindObject(
                    "hPhotTrigSM{}TRU{}".format(sm, tru))
            })

    return output


def integrate(hist, trigger_threshold=4):
    return hist.Integral(hist.FindBin(trigger_threshold), hist.GetNbinsX())


def turnon_level(hist, trigger_threshold=4, trigger_max=50):
    func = ROOT.TF1("func", "pol0", trigger_threshold, trigger_max)
    func.SetParameter(0, 1)
    # hist.GetXaxis().SetRangeUser(trigger_threshold, trigger_max)
    hist.Fit(func, "RL")
    # hist.Draw()
    # ROOT.gPad.Update()
    # raw_input()
    # print func.GetParameter(0)
    # assert False
    return func.GetParameter(0)


def read_dataset(filepath, rules):
    infile = ROOT.TFile(filepath)
    infile.ls()
    outputs = []
    for key in infile.GetListOfKeys():
        outputs += row_decoder(key)
    return pd.DataFrame(outputs)


def report(x):
    d = {}
    d["nruns"] = len(x["run"])
    d["integra_hist"] = trendhist(x["run"], x["integral"])
    d["efficiency_hist"] = trendhist(x["run"], x["efficiency"])
    return pd.Series(d, index=["nruns", "integra_hist", "efficiency_hist"])


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

        title = "Number of 4x4 patches per run SM{}".format(sm)
        title += ";; # patches / accepntace/ #events"

        plotter = Plotter()
        plotter.plot(sm_hists["integra_hist"],
                     sm_hists["tru"],
                     canvas.cd(1),
                     title)

        plotter.plot(sm_hists["integra_hist"],
                     sm_hists["tru"],
                     canvas.cd(2),
                     title)

        save_canvas(canvas, "trending-tru-sm-{}".format(sm))
        canvas.Update()
        raw_input()
