import ROOT
import numpy as np
from contextlib import contextmanager

import spectrum.broot as br
import spectrum.sutils as su


@contextmanager
def style():
    old_style = ROOT.gStyle.Clone("modern")
    style = ROOT.gStyle.Clone("alice")
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

    style.SetTitleOffset(1.0, "X")
    style.SetTitleOffset(1.0, "Y")

    # style.SetFillColor(ROOT.kWhite)
    style.SetTitleFillColor(ROOT.kWhite)

    style.SetOptDate(0)
    style.SetOptTitle(0)
    style.SetOptStat(0)
    style.SetOptFit(111)
    style.cd()
    yield style
    old_style.cd()


def legend(data):
    legend = ROOT.TLegend(0.6, 0.7, 0.8, 0.85)
    legend.SetBorderSize(0)
    for entry in data:
        legend.AddEntry(entry, entry.GetTitle(), "p")
    legend.SetFillColor(0)
    legend.SetTextColor(1)
    legend.SetTextSize(0.035)
    return legend


def separate(data):
    hists, graphs, functions = [], [], []
    for entry in data:
        if issubclass(type(entry), ROOT.TH1):
            hists.append(entry)
        if issubclass(type(entry), ROOT.TF1):
            functions.append(entry)
        if issubclass(type(entry), ROOT.TGraph):
            functions.append(entry)
    return hists, graphs, functions


def plot(data, xtitle=None, ytitle=None, logx=True, logy=True, stop=True):
    hists, graphs, functions = separate(data)
    histogrammed = (
        hists +
        list(map(lambda x: x.GetHistogram(), functions)) +
        list(map(br.graph2hist, graphs))
    )
    x = np.concatenate([br.bins(h).centers for h in histogrammed])
    y = np.concatenate([br.bins(h).contents for h in histogrammed])

    box = ROOT.TH1F("box", "Test test test", 1000, min(x), max(x))
    box.GetXaxis().SetTitle(xtitle or data[0].GetXaxis().GetTitle())
    box.GetYaxis().SetTitle(ytitle or data[0].GetYaxis().GetTitle())
    box.SetAxisRange(min(x) * 0.95, max(x) * 1.05, "X")
    box.SetAxisRange(min(y) * 0.95, max(y) * 1.05, "Y")
    box.GetXaxis().SetMoreLogLabels(True)

    graphed = graphs + list(map(br.hist2graph, hists))
    with style(), su.canvas(stop=stop) as canvas:
        canvas.SetLeftMargin(0.15)
        canvas.SetRightMargin(0.05)
        canvas.SetLogx(logx)
        canvas.SetLogy(logy)
        box.Draw()
        su.ticks(canvas)
        for i, graph in enumerate(graphed):
            color = br.icolor(i)
            graph.SetMarkerStyle(20)
            graph.SetMarkerSize(1)
            graph.SetLineColor(color)
            graph.SetMarkerColor(color)
            graph.Draw("p")

        for i, func in enumerate(functions):
            # Don't use colors for graphs
            # func.SetLineColor(br.icolor(i, offset=len(graphed)))
            func.Draw("same")

        ll = legend(graphed + functions)
        ll.Draw("same")
