import ROOT

INDEX_COLOR = {
    1: ROOT.kRed + 1,
    2: ROOT.kGreen + 1,
    3: ROOT.kBlue + 1,
    4: ROOT.kOrange + 1,
}


def decorate_hist(hist):
    hist.SetTitleOffset(0.3, "Y")
    hist.SetTickLength(0.01, "Y")
    hist.SetLabelSize(0.06, "XY")
    hist.SetTitleSize(0.06, "XY")
    return hist


def plot(hists, labels=None, pad=None):
    assert labels is None or len(hists) == len(labels), "Wrong length"
    if pad is not None:
        pad.cd()

    # Draw multiple
    stack = ROOT.THStack()
    for i, hist in enumerate(hists):
        hist.SetLineColor(INDEX_COLOR.get(i + 1, 1))
        stack.Add(decorate_hist(hist))
    stack.Draw("nostack")

    # Set labels
    if labels is not None:
        legend = ROOT.TLegend(0.55, 0.8, 0.9, 0.9)
        legend.SetBorderSize(0)
        legend.SetFillStyle(0)
        legend.SetTextSize(0.04)
        for hist, label in zip(hists, labels):
            legend.AddEntry(hist, label)
        legend.Draw("same")

    ROOT.gPad.SetLeftMargin(0.06)
    ROOT.gPad.SetRightMargin(0.02)
    ROOT.gPad.SetTopMargin(0.10)
    ROOT.gPad.SetBottomMargin(0.14)

    ROOT.gPad.SetGridx()
    ROOT.gPad.SetGridy()
    ROOT.gPad.SetTickx()
    ROOT.gPad.SetTicky()

    if pad is not None:
        return [stack, legend]
    raw_input("Press enter to continue")


class Plotter(object):
    def __init__(self):
        super(Plotter, self).__init__()
        self.cache = []

    def plot(self, hist, labels=None, pad=None):
        self.cache.append(plot(hist, labels, pad))
