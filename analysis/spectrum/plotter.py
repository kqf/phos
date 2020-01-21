from contextlib import contextmanager

import six
import numpy as np
import ROOT
import seaborn as sns
import spectrum.broot as br
import spectrum.sutils as su
from repoze.lru import lru_cache


@contextmanager
def pcanvas(name="cn", size=(96, 128), stop=True, scale=6, oname=None):
    canvas = ROOT.TCanvas(name, "canvas",
                          int(size[0] * scale), int(size[1] * scale))
    canvas.SetTickx()
    canvas.SetTicky()
    canvas.SetGridx()
    canvas.SetGridy()

    old = ROOT.gROOT.IsBatch()
    ROOT.gROOT.SetBatch(not stop)
    yield canvas
    canvas.Update()
    if oname is not None:
        canvas.SaveAs(su.ensure_directory(oname))

    if not stop:
        return
    canvas.Connect("Closed()", "TApplication",
                   ROOT.gApplication, "Terminate()")
    ROOT.gApplication.Run(True)
    ROOT.gROOT.SetBatch(old)


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
def adjust_canas(data, xlimits, ylimits, xtitle, ytitle, yoffset, more_logs):
    x = xlimits or np.concatenate([br.edges(h) for h in data])
    y = ylimits or np.concatenate([br.bins(h).contents for h in data])
    box = ROOT.TH1F("box", "", 1000, min(x), max(x))
    box.SetAxisRange(min(x) * 0.95, max(x) * 1.05, "X")
    box.SetAxisRange(min(y) * 0.95, max(y) * 1.05, "Y")
    box.GetXaxis().SetTitle(xtitle or data[0].GetXaxis().GetTitle())
    box.GetYaxis().SetTitle(ytitle or data[0].GetYaxis().GetTitle())
    box.GetXaxis().SetMoreLogLabels(more_logs)
    box.GetYaxis().SetTitleOffset(yoffset)
    box.Draw()
    return box


@lru_cache(maxsize=1024)
def define_color(r, g, b, alpha=1):
    colorindex = ROOT.TColor.GetFreeColorIndex()
    color = ROOT.TColor(colorindex, r, g, b)
    return colorindex, color


def ensure_options(ngraphs, options):
    if isinstance(options, six.string_types):
        return [options] * ngraphs
    return options


@lru_cache(maxsize=1024)
def _draw_graph(i, graph, colors, option, ngraphs):
    graph = graph.Clone()

    if colors == 'auto':
        color, marker = br.auto_color_marker(i)
        graph.SetMarkerStyle(marker)
        graph.SetMarkerSize(1)
        graph.SetLineColor(color)
        graph.SetFillColor(color)
        graph.SetFillColorAlpha(color, 0.50)
        graph.SetMarkerColor(color)
    if colors == 'levels':
        alpha = np.logspace(0, 0.9, ngraphs)[i]
        graph.SetMarkerStyle(20)
        graph.SetMarkerSize(1)
        graph.SetLineColorAlpha(ROOT.kRed + 1, alpha)
        graph.SetFillColorAlpha(ROOT.kRed + 1, alpha)
        graph.SetMarkerColorAlpha(ROOT.kRed + 1, alpha)
    if colors == 'coolwarm':
        palette = sns.color_palette("coolwarm", ngraphs)
        color, _ = define_color(*palette[i])
        graph.SetMarkerStyle(20)
        graph.SetMarkerSize(1)
        graph.SetLineColor(color)
        graph.SetFillColor(color)
        graph.SetMarkerColor(color)

    if "e5" in option.lower():
        graph.SetFillColor(ROOT.kWhite)

    # Remove x-errors for tgraph styled plots
    if "e5" not in option.lower():
        for point in range(graph.GetN()):
            graph.SetPointError(point, 0, graph.GetErrorY(point))

    graph.Draw(option)
    return graph


@lru_cache(maxsize=1024)
def _draw_histogram(i, hist, colors, nhists=1):
    if colors == 'auto':
        color, marker = br.auto_color_marker(i)
        hist.SetLineColor(color)
        hist.SetMarkerColor(color)
    if colors == 'levels':
        alpha = np.logspace(0, 0.9, nhists)[i]
        hist.SetLineColorAlpha(ROOT.kRed + 1, alpha)
        hist.SetMarkerColorAlpha(ROOT.kRed + 1, alpha)
    if colors == 'coolwarm':
        palette = sns.color_palette("coolwarm", nhists)
        color, _ = define_color(*palette[i])
        hist.SetLineColor(color)
        hist.SetMarkerColor(color)
    hist.SetFillStyle(0)
    hist.SetMarkerStyle(20)
    hist.SetMarkerSize(1)
    hist.Draw("same hist")
    return hist


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
    options="p"
):
    hists, graphs, functions = separate(data)
    histogrammed = (
        hists +
        list(map(lambda x: x.GetHistogram(), functions)) +
        list(map(br.graph2hist, graphs))
    )
    graphed = graphs + list(map(br.hist2graph, hists))
    with style(), pcanvas(size=csize, stop=stop, oname=oname) as canvas:
        canvas.SetLeftMargin(0.15)
        canvas.SetRightMargin(0.05)
        canvas.SetLogx(logx)
        canvas.SetLogy(logy)
        adjust_canas(
            tuple(histogrammed),
            xlimits,
            ylimits,
            xtitle,
            ytitle,
            yoffset,
            more_logs
        )
        options = ensure_options(len(graphed), options)
        plotted = []
        for i, (graph, option) in enumerate(zip(graphed, options)):
            plotted.append(
                _draw_graph(i, graph, colors, option, len(graphed))
            )

        for i, func in enumerate(functions):
            plotted.append(func)
            func.Draw("same " + func.GetDrawOption())

        if legend_pos is not None:
            ll = legend(plotted, legend_pos, ltitle, ltext_size)
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
    with style(), pcanvas("cn", size=csize, stop=stop, oname=oname) as canvas:
        canvas.SetLeftMargin(0.15)
        canvas.SetRightMargin(0.05)
        canvas.SetLogx(logx)
        canvas.SetLogy(logy)
        adjust_canas(
            tuple(data),
            xlimits,
            ylimits,
            xtitle,
            ytitle,
            yoffset,
            more_logs
        )
        plotted = []
        for i, hist in enumerate(data):
            plotted.append(
                _draw_histogram(i, hist, colors, len(data))
            )

        if legend_pos is not None:
            ll = legend(plotted, legend_pos, ltitle, ltext_size)
            ll.Draw("same")
