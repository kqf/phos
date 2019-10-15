import ROOT
import numpy as np
from contextlib import contextmanager

import spectrum.broot as br
import spectrum.sutils as su


@contextmanager
def style():
    optdate = ROOT.gStyle.GetOptDate()
    opttitle = ROOT.gStyle.GetOptTitle()
    optstat = ROOT.gStyle.GetOptStat()
    optfit = ROOT.gStyle.GetOptFit()

    ROOT.gStyle.SetOptDate(0)
    ROOT.gStyle.SetOptTitle(0)
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetOptFit(0)

    yield
    print("exit")
    ROOT.gStyle.SetOptDate(optdate)
    ROOT.gStyle.SetOptTitle(opttitle)
    ROOT.gStyle.SetOptStat(optstat)
    ROOT.gStyle.SetOptFit(optfit)


def plot(data, xtitle, ytitle, logx=True, logy=True):
    x = np.concatenate([br.bins(h).centers for h in data])
    y = np.concatenate([br.bins(h).contents for h in data])

    box = ROOT.TH1F("box", "", 1000, 0, 20)
    box.GetXaxis().SetTitle(xtitle)
    box.GetYaxis().SetTitle(ytitle)
    box.SetAxisRange(min(x) * 0.95, max(x) * 1.05, "X")
    box.SetAxisRange(min(y) * 0.95, max(y) * 1.05, "Y")

    graphs = list(map(br.hist2graph, data))
    with style(), su.canvas() as canvas:
        canvas.SetLeftMargin(0.15)
        canvas.SetRightMargin(0.05)
        canvas.SetLogx(logx)
        canvas.SetLogy(logy)
        box.Draw()
        for i, graph in enumerate(graphs):
            color = br.icolor(i)
            graph.SetMarkerStyle(20)
            graph.SetMarkerSize(1)
            graph.SetLineColor(color)
            graph.SetMarkerColor(color)
            graph.Draw("p")
