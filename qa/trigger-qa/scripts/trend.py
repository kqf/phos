import ROOT
import pandas as pd
import plotting
pd.set_option('display.expand_frame_repr', False)

filepath = "../../../neutral-meson-spectra/" \
    "input-data/data/LHC16/trigger_qa/iteration2/LHC16g-pass1.root"


def remove_empty_runs(hist):
    runs, counts = [], []
    for i in range(1, hist.GetNbinsX() + 1):
        if not hist.GetBinContent(i) > 0:
            continue
        runs.append(hist.GetBinCenter(i))
        counts.append(hist.GetBinContent(i))
    reduced = ROOT.TH1F(
        hist.GetName() + "_reduced",
        hist.GetTitle(),
        len(runs), 0, len(runs))

    for i, (r, c) in enumerate(zip(runs, counts)):
        reduced.SetBinContent(i + 1, c)
        reduced.GetXaxis().SetBinLabel(i + 1, str(int(r)))
    return reduced


def average(hists):
    total = hists[0].Clone("average")
    total.Reset()
    for hist in hists:
        total.Add(hist)
    total.Scale(1. / len(hists))
    return total


def scale_for_acceptance(hists, badmap_fname="BadMap_LHC16-updated.root"):
    if not badmap_fname:
        return hists
    badmap = ROOT.TFile(badmap_fname)
    for i, hist in enumerate(hists):
        mod = i + 1
        sm = badmap.Get("PHOS_BadMap_mod{}".format(mod))
        bad_channels = sm.GetEntries()
        all_channels = sm.GetNbinsX() * sm.GetNbinsY()
        hist.Scale(1. / (all_channels - bad_channels))
    return hist


def main(nmodules=4):
    l0 = ROOT.TFile(filepath).Get("PHOSTriggerQAResultsL0")
    outputs = pd.DataFrame(index=map("SM{}".format, range(1, nmodules + 1)))
    histname = "hRunMatchedTriggers"
    outputs[histname] = [
        l0.FindObject("{}{}".format(histname, str(i)))
        for i in outputs.index
    ]
    outputs["cleaned"] = outputs[histname].apply(remove_empty_runs)
    scale_for_acceptance(outputs["cleaned"].values)
    outputs = outputs.append(pd.DataFrame([{
        "cleaned": average(outputs["cleaned"].values)
    }], index=["average"]), sort=True)

    plotting.plot(outputs["cleaned"].values, outputs.index)


if __name__ == '__main__':
    main()
