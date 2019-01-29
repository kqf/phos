import ROOT

INDEX_COLOR = {
    1: ROOT.kRed + 1,
    2: ROOT.kOrange + 1,
    4: ROOT.kYellow + 1,
    5: ROOT.kGreen + 1,
    6: ROOT.kBlue + 1,
    7: ROOT.kViolet + 1,
    8: ROOT.kPink + 1,
}


def decorate_hist(hist):
    hist.SetTitleOffset(0.3, "Y")
    hist.SetTickLength(0.01, "Y")
    hist.SetLabelSize(0.06, "XY")
    hist.SetTitleSize(0.06, "XY")
    return hist


def decorate_pad(pad):
    pad.SetGridx()
    pad.SetGridy()
    pad.SetTickx()
    pad.SetTicky()
    return pad


def plot(hists, labels=None, pad=None, title=None):
    assert labels is None or len(hists) == len(labels), "Wrong length"
    if pad is not None:
        pad.cd()

    # Draw multiple
    stack = ROOT.THStack()
    for i, hist in enumerate(hists):
        hist.SetLineColor(INDEX_COLOR.get(i + 1, 1))
        stack.Add(decorate_hist(hist))
        stack.SetTitle(hist.GetTitle())

    if title is not None:
        stack.SetTitle(title)
    stack.Draw("nostack")

    # Set labels
    if labels is not None:
        legend = ROOT.TLegend(0.55, 0.66, 0.9, 0.86)
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
    decorate_pad(ROOT.gPad)

    if pad is not None:
        pad.cached = [stack, legend]
        return pad.cached
    save_canvas(ROOT.gPad, hists[0].GetName())
    raw_input("Press enter to continue")


def save_canvas(canvas, name):
    canvas.SaveAs(name + ".pdf")
    # canvas.SaveAs(name + ".png")
    ofile = ROOT.TFile(name + ".root", "recreate")
    canvas.Write()
    ofile.Write()


class Plotter(object):
    def __init__(self):
        super(Plotter, self).__init__()
        self.cache = []

    def plot(self, hist, labels=None, pad=None, title=None):
        self.cache.append(plot(hist, labels, pad, title))
