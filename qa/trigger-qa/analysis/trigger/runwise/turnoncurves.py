import ROOT
import pandas as pd
from sklearn.pipeline import make_pipeline
from trigger.transformators import RatioCalculator
from trigger.transformators import RebinTransformer
from trigger.transformators import FunctionTransformer


def row_decoder(listkey, sm_start=1, sm_stop=4, tru_start=1, tru_stop=8):
    lst, output = listkey.ReadObj(), []

    for sm in range(sm_start, sm_stop + 1):
        for tru in range(tru_start, tru_stop + 1):
            output.append({
                "name": listkey.GetName(),
                "module": "SM{}".format(sm),
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


def turnon_stats(filepath):
    df = read_dataset(filepath, rules=row_decoder)
    analysis = make_pipeline(
        RebinTransformer("hPhotAll", "all_rebinned"),
        RebinTransformer("hPhotTrig", "matched_rebinned"),
        RatioCalculator(["matched_rebinned", "all_rebinned"], "turnon"),
        # FunctionTransformer("turnon", "integral", integrate),
        FunctionTransformer("turnon", "efficiency", turnon_level)
    )
    print analysis.fit_transform(df)
