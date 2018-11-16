import ROOT

filepath = "../../../neutral-meson-spectra/" \
    "input-data/data/LHC16/trigger_qa/iteration2/LHC16g-pass1.root"

INDEX_COLOR = {
    1: ROOT.kRed + 1,
    2: ROOT.kGreen + 1,
    3: ROOT.kBlue + 1,
    4: ROOT.kOrange + 1,
}


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
    l0.ls()
    matched_triggers_modules = [
        l0.FindObject("hRunMatchedTriggersSM{}".format(i))
        for i in range(1, nmodules + 1)
    ]
    reduced = map(remove_empty_runs, matched_triggers_modules)
    scale_for_acceptance(reduced)
    reduced.append(average(reduced))
    stack = ROOT.THStack()

    for i, hist in enumerate(reduced):
        hist.SetLineColor(INDEX_COLOR.get(i + 1, 1))
        stack.Add(hist)

    map(stack.Add, reduced)
    stack.Draw("nostack")
    raw_input("test test test ...")


if __name__ == '__main__':
    main()
