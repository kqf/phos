import ROOT
import json
import numpy as np

from sutils import wait, gcanvas, Cc, adjust_canvas, adjust_labels
from broot import BROOT as br


class VisHub(object):

    def __init__(self, *args, **kwargs):
        super(VisHub, self).__init__()
        self.double = Visualizer(*args, **kwargs)
        self.regular = MultipleVisualizer(*args, **kwargs)

    def compare_visually(self, hists, ci):
        if len(hists) == 2:
            return self.double.compare_visually(hists, ci)
        return self.regular.compare_visually(hists, ci)


class MultipleVisualizer(object):
    # TODO: replace with a function
    markers = {i: 20 + i for i in range(7)}

    def __init__(self, size, rrange, crange, stop, oname):
        super(MultipleVisualizer, self).__init__()
        self.size = size
        self.cache = []
        self.rrange = rrange
        self.crange = crange
        self.output_prefix = 'compared-'
        self.ignore_ratio = self.rrange and (self.rrange[0] < 0 or self.rrange[1] < 0)
        self.oname = oname
        self.stop = stop
        
    @br.init_inputs
    def compare_visually(self, hists, ci, pad = None):
        # TODO: Add tests for a single histogram
        # if len(hists) == 1: # adjust_canvas(canvas)
        legend = ROOT.TLegend(0.7, 0.4, 0.8, 0.6)
        legend.SetBorderSize(0)
        legend.SetFillStyle(0)
        legend.SetTextSize(0.04)

        mainpad = pad if pad else gcanvas()
        mainpad.cd()
        mainpad.SetGridx()
        mainpad.SetGridy()

        first_hist = sorted(hists, key=lambda x: x.priority)[0]
        mainpad.SetLogx(first_hist.logx)
        mainpad.SetLogy(first_hist.logy)
        first_hist.SetStats(False)

        if self.crange:
            first_hist.SetAxisRange(self.crange[0], self.crange[1] , 'Y')
        first_hist.DrawCopy()

        for i, h in enumerate(hists): 
            h.SetStats(False)
            h.SetLineColor(ci + i)
            h.SetFillColor(ci + i)
            mstyle = self.markers.get(h.marker, 20)
            h.SetMarkerStyle(mstyle)
            h.SetMarkerColor(ci + i)
            h.DrawCopy('same')
            legend.AddEntry(h, h.label)
        legend.Draw('same')

        ROOT.gStyle.SetOptStat(0)
        mainpad.SetTickx()
        mainpad.SetTicky() 

        self.cache.append(legend)

        if pad:
            return None

        fname = hists[0].GetName() + '-' + '-'.join(x.label for x in hists) 
        oname = self.get_oname(fname.lower())
        wait(oname, save=True, draw=self.stop)
        return None


    def draw_ratio(self, hists, pad):
        return None


    def get_oname(self, name):
        if self.oname:
            return self.oname

        oname = self.output_prefix + name
        return oname

        
class Visualizer(MultipleVisualizer):
    def __init__(self, size, rrange, crange, stop, oname):
        super(Visualizer, self).__init__(size, rrange, crange, stop, oname)

    def _canvas(self, hists):
        c1 = gcanvas(self.size[0], self.size[1], resize = True)
        c1.Clear()

        if self.ignore_ratio:
            return c1, c1, c1

        pad1 = ROOT.TPad("pad1","main plot", 0, 0.3, 1, 1);
        pad1.SetBottomMargin(0);
        pad1.Draw()
        c1.cd()
        pad2 = ROOT.TPad("pad2","ratio", 0, 0, 1, 0.3);
        pad2.SetTopMargin(0);
        pad2.SetBottomMargin(0.2);
        pad2.Draw();
        pad2.SetTickx()
        pad2.SetTicky()
        pad2.SetGridy()
        pad2.SetGridx()
        return c1, pad1, pad2

    def draw_ratio(self, hists, pad):
        if self.ignore_ratio:
            return None

        try:
            a, b = hists
            ratio = br.ratio(a, b)
        except ValueError:
            return None
        # Add this to cache othervise the 
        # histogram will be deleted automatically by ROOT
        self.cache.append(ratio)

        pad.cd()
        adjust_labels(ratio, hists[0], scale = 7./3)
        ratio.GetYaxis().CenterTitle(True)
        self.fit_ratio(ratio)
        self.set_ratio_yaxis(ratio)

        ROOT.gPad.SetGridy()
        ratio.Draw()
        return ratio 

    def set_ratio_yaxis(self, ratio, n = 3):
        if self.rrange: 
            ratio.SetAxisRange(self.rrange[0], self.rrange[1] , 'Y')
            return

        bins = np.array([ratio.GetBinContent(i) for i in range(1, ratio.GetXaxis().GetNbins())])
        mean, std = np.mean(bins), np.std(bins)
        no_outliers = [b for b in bins if abs(b - mean) < n * std]

        if not no_outliers:
            return

        a, b = min(no_outliers), max(no_outliers)
        ratio.SetAxisRange(a, b , 'Y')


    def _fit(self, ratio):
        # Add fitfunc as an attribute to
        # the numerator histogram to get the output
        ratio.Fit(ratio.fitfunc, "Rq")
        ratio.fitfunc.SetLineColor(38)
        ratio.SetStats(True)

    def fit_ratio(self, ratio):
        try:
            self._fit(ratio)
        except AttributeError: # there is no fitfunc defined
            return

        ROOT.gStyle.SetStatFontSize(0.1)
        ROOT.gStyle.SetOptStat('')
        ROOT.gStyle.SetStatX(0.35)
        ROOT.gStyle.SetStatW(0.1)
        ROOT.gStyle.SetStatStyle(0)
        ROOT.gStyle.SetStatBorderSize(0)
        ROOT.gStyle.SetOptFit(1)


    def compare_visually(self, hists, ci):
        canvas, mainpad, ratiopad = self._canvas(hists)

        super(Visualizer, self).compare_visually(hists, ci, mainpad)
        ratio = self.draw_ratio(hists, ratiopad)

        # ctrl+alt+f4 closes enire canvas not just a pad.
        canvas.cd()
        fname = hists[0].GetName() + '-' + '-'.join(x.label for x in hists) 
        oname = self.get_oname(fname.lower())
        wait(oname, save=True, draw=self.stop)
        return adjust_labels(ratio, hists[0])

