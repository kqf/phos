import ROOT

INDEX_COLOR = {
    1: ROOT.kRed + 1,
    2: ROOT.kGreen + 1,
    3: ROOT.kBlue + 1,
    4: ROOT.kOrange + 1,
}


def plot(hists, labels=None):
    assert labels is None or len(hists) == len(labels), "Wrong length"
    stack = ROOT.THStack()

    for i, hist in enumerate(hists):
        hist.SetLineColor(INDEX_COLOR.get(i + 1, 1))
        stack.Add(hist)
    map(stack.Add, hists)
    stack.Draw("nostack")
    if labels is not None:
        legend = ROOT.TLegend(0.55, 0.8, 0.9, 0.9)
        legend.SetBorderSize(0)
        legend.SetFillStyle(0)
        legend.SetTextSize(0.04)
        for hist, label in zip(hists, labels):
            legend.AddEntry(hist, label)
        legend.Draw("same")

    ROOT.gPad.SetTicky()
    ROOT.gPad.SetTickx()
    ROOT.gPad.SetGridx()
    ROOT.gPad.SetGridy()
    ROOT.gPad.Update()
    raw_input("Press enter to continue")
