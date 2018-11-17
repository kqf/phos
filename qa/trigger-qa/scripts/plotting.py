import ROOT

INDEX_COLOR = {
    1: ROOT.kRed + 1,
    2: ROOT.kGreen + 1,
    3: ROOT.kBlue + 1,
    4: ROOT.kOrange + 1,
}


def plot(hists):
    stack = ROOT.THStack()

    for i, hist in enumerate(hists):
        hist.SetLineColor(INDEX_COLOR.get(i + 1, 1))
        stack.Add(hist)

    map(stack.Add, hists)
    stack.Draw("nostack")
    raw_input("Press enter to continue")
