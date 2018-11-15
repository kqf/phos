import ROOT

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


def main():
    l0 = ROOT.TFile(filepath).Get("PHOSTriggerQAResultsL0")
    l0.ls()
    matched_triggers = l0.FindObject("hRunMatchedTriggersSM2")
    reduced = remove_empty_runs(matched_triggers)
    reduced.Draw()
    raw_input("test test test ...")


if __name__ == '__main__':
    main()
