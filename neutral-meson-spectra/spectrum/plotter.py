from contextlib import contextmanager

import numpy as np
import ROOT
import seaborn as sns
import spectrum.broot as br
import spectrum.sutils as su
from repoze.lru import lru_cache


@contextmanager
def pcanvas(name="cn", size=(96, 128), stop=False, scale=6, oname=None):
    canvas = ROOT.TCanvas(name, "canvas",
                          int(size[0] * scale), int(size[1] * scale))
    canvas.SetTickx()
    canvas.SetTicky()
    canvas.SetGridx()
    canvas.SetGridy()

    yield canvas
    canvas.Update()
    if oname is not None:
        canvas.SaveAs(su.ensure_directory(oname))

    if not stop:
        return
    canvas.Connect("Closed()", "TApplication",
                   ROOT.gApplication, "Terminate()")
    ROOT.gApplication.Run(True)


@contextmanager
def style():
    # old_style = ROOT.gStyle.Clone("modern")
    style = ROOT.gStyle  # .Clone("alice")
    style.SetOptDate(0)
    style.SetOptTitle(0)
    style.SetOptStat(0)
    style.SetOptFit(0)

    style.SetPalette(1)
    style.SetCanvasBorderMode(-1)
    style.SetCanvasBorderSize(1)
    style.SetCanvasColor(10)

    style.SetFrameFillColor(10)
    style.SetFrameBorderSize(1)
    style.SetFrameBorderMode(-1)
    style.SetFrameLineWidth(1)
    style.SetFrameLineColor(1)

    style.SetHistFillColor(0)
    style.SetHistLineWidth(2)
    style.SetHistLineColor(1)

    style.SetPadColor(10)
    style.SetPadBorderSize(1)
    style.SetPadBorderMode(-1)

    style.SetStatColor(10)
    style.SetTitleColor(ROOT.kBlack, "X")
    style.SetTitleColor(ROOT.kBlack, "Y")

    style.SetLabelSize(0.04, "X")
    style.SetLabelSize(0.04, "Y")
    style.SetLabelSize(0.04, "Z")
    style.SetTitleSize(0.04, "X")
    style.SetTitleSize(0.04, "Y")
    style.SetTitleSize(0.04, "Z")
    style.SetTitleFont(62, "X")
    style.SetTitleFont(62, "Y")
    style.SetTitleFont(62, "Z")
    style.SetLabelFont(42, "X")
    style.SetLabelFont(42, "Y")
    style.SetLabelFont(42, "Z")
    style.SetStatFont(42)

    style.SetTitleOffset(1.2, "X")
    style.SetTitleOffset(1.2, "Y")

    # style.SetFillColor(ROOT.kWhite)
    style.SetTitleFillColor(ROOT.kWhite)

    style.SetOptDate(0)
    style.SetOptTitle(0)
    style.SetOptStat(0)
    style.SetOptFit(111)
    style.cd()
    yield style
    # old_style.cd()


def legend(data, coordinates, ltitle=None, ltext_size=0.035):
    legend = ROOT.TLegend(*coordinates)
    legend.SetBorderSize(0)

    if ltitle is not None:
        legend.AddEntry(0, ltitle, "")

    for entry in data:
        options = "f" if entry.GetFillStyle() > 1000 else "pl"
        legend.AddEntry(entry, entry.GetTitle(), options)

    legend.SetFillColor(0)
    legend.SetTextColor(1)
    legend.SetTextSize(ltext_size)
    return legend


def separate(data):
    hists, graphs, functions = [], [], []
    for entry in data:
        if issubclass(type(entry), ROOT.TH1):
            hists.append(entry)
        if issubclass(type(entry), ROOT.TF1):
            functions.append(entry)
        if issubclass(type(entry), ROOT.TGraph):
            graphs.append(entry)
    return hists, graphs, functions


@lru_cache(maxsize=1024)
def define_color(r, g, b, alpha=1):
    colorindex = ROOT.TColor.GetFreeColorIndex()
    color = ROOT.TColor(colorindex, r, g, b)
    return colorindex, color


def plot(
    data,
    xtitle=None,
    ytitle=None,
    logx=True,
    logy=True,
    stop=True,
    xlimits=None,
    ylimits=None,
    csize=(96, 128),
    oname=None,
    legend_pos=(0.6, 0.7, 0.8, 0.85),
    ltitle=None,
    more_logs=True,
    yoffset=1.2,
    colors='auto',
    ltext_size=0.035,
):
    hists, graphs, functions = separate(data)
    histogrammed = (
        hists +
        list(map(lambda x: x.GetHistogram(), functions)) +
        list(map(br.graph2hist, graphs))
    )
    x = xlimits or np.concatenate([br.bins(h).centers for h in histogrammed])
    y = ylimits or np.concatenate([br.bins(h).contents for h in histogrammed])

    graphed = graphs + list(map(br.hist2graph, hists))
    with style(), pcanvas(size=csize, stop=stop, oname=oname) as canvas:
        box = ROOT.TH1F("box", "", 1000, min(x) * 0.95, max(x) * 1.05)
        box.GetXaxis().SetTitle(xtitle or data[0].GetXaxis().GetTitle())
        box.GetYaxis().SetTitle(ytitle or data[0].GetYaxis().GetTitle())
        box.SetAxisRange(min(x) * 0.95, max(x) * 1.05, "X")
        box.SetAxisRange(min(y) * 0.95, max(y) * 1.05, "Y")
        box.GetXaxis().SetMoreLogLabels(more_logs)
        box.GetYaxis().SetTitleOffset(yoffset)

        canvas.SetLeftMargin(0.15)
        canvas.SetRightMargin(0.05)
        canvas.SetLogx(logx)
        canvas.SetLogy(logy)
        box.Draw()
        for i, graph in enumerate(graphed):
            if colors == 'auto':
                color, marker = br.auto_color_marker(i)
                graph.SetMarkerStyle(marker)
                graph.SetMarkerSize(1)
                graph.SetLineColor(color)
                graph.SetFillColor(color)
                graph.SetFillColorAlpha(color, 0.50)
                graph.SetMarkerColor(color)

            if colors == 'levels':
                alpha = np.logspace(0, 0.9, len(graphed))[i]
                graph.SetMarkerStyle(20)
                graph.SetMarkerSize(1)
                graph.SetLineColorAlpha(ROOT.kRed + 1, alpha)
                graph.SetFillColorAlpha(ROOT.kRed + 1, alpha)
                graph.SetMarkerColorAlpha(ROOT.kRed + 1, alpha)

            if colors == 'coolwarm':
                palette = sns.color_palette("coolwarm", len(graphed))
                color, _ = define_color(*palette[i])
                graph.SetMarkerStyle(20)
                graph.SetMarkerSize(1)
                graph.SetLineColor(color)
                graph.SetFillColor(color)
                graph.SetMarkerColor(color)

            options = graph.GetDrawOption() or "p"
            graph.Draw(options)

        for i, func in enumerate(functions):
            func.Draw("same " + func.GetDrawOption())

        if legend_pos is not None:
            ll = legend(graphed + functions, legend_pos, ltitle, ltext_size)
            ll.Draw("same")


def hplot(
    data,
    xtitle=None,
    ytitle=None,
    logx=True,
    logy=True,
    stop=True,
    xlimits=None,
    ylimits=None,
    csize=(96, 128),
    oname=None,
    legend_pos=(0.6, 0.7, 0.8, 0.85),
    ltitle=None,
    more_logs=True,
    yoffset=1.2,
    colors='auto',
    ltext_size=0.035,
):
    x = xlimits or np.concatenate([br.edges(h) for h in data])
    y = ylimits or np.concatenate([br.bins(h).contents for h in data])

    with style(), pcanvas("cn", size=csize, stop=stop, oname=oname) as canvas:
        box = ROOT.TH1F("box", "", 1000, min(x), max(x))
        box.GetXaxis().SetTitle(xtitle or data[0].GetXaxis().GetTitle())
        box.GetYaxis().SetTitle(ytitle or data[0].GetYaxis().GetTitle())
        box.SetAxisRange(min(x) * 0.95, max(x) * 1.05, "X")
        box.SetAxisRange(min(y) * 0.95, max(y) * 1.05, "Y")
        box.GetXaxis().SetMoreLogLabels(more_logs)
        box.GetYaxis().SetTitleOffset(yoffset)

        canvas.SetLeftMargin(0.15)
        canvas.SetRightMargin(0.05)
        canvas.SetLogx(logx)
        canvas.SetLogy(logy)
        box.Draw()
        for i, hist in enumerate(data):
            if colors == 'auto' and hist.GetLineColor() < 0:
                color, marker = br.auto_color_marker(i)
                hist.SetLineColor(color)
                hist.SetMarkerColor(color)

            if colors == 'levels' and hist.GetLineColor() < 0:
                alpha = np.logspace(0, 0.9, len(data))[i]
                hist.SetLineColorAlpha(ROOT.kRed + 1, alpha)
                hist.SetMarkerColorAlpha(ROOT.kRed + 1, alpha)

            if colors == 'coolwarm' and hist.GetLineColor() < 0:
                palette = sns.color_palette("coolwarm", len(data))
                color, _ = define_color(*palette[i])
                hist.SetLineColor(color)
                hist.SetMarkerColor(color)

            hist.SetFillStyle(0)
            hist.SetMarkerStyle(20)
            hist.SetMarkerSize(1)
            # hist.SetLineWidth(2)
            hist.Draw("same hist")

        if legend_pos is not None:
            ll = legend(data, legend_pos, ltitle, ltext_size)
            ll.Draw("same")
