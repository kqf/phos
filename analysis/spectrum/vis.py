from __future__ import print_function
import ROOT
import numpy as np

import spectrum.broot as br
import spectrum.sutils as su
import spectrum.plotter as plt


def calculate_x_limits(hists):
    data = np.array([br.hist_range(h) for h in hists])
    return data.min() * 0.95, data.max() * 1.05


def set_pad_logx(hist, pad):
    if 'eff' in hist.GetName().lower():
        return

    hist.GetXaxis().SetMoreLogLabels(True)
    if hist.logx is not None:
        pad.SetLogx(hist.logx)
        return

    # Draw logx for increasing bin width
    start_width = hist.GetBinWidth(1)
    stop_width = hist.GetBinWidth(hist.GetNbinsX() - 1)
    pad.SetLogx(start_width < stop_width)

    if hist.GetName() == 'testtest':
        print(hist, start_width < stop_width)


def set_pad_logy(hist, pad):
    if 'eff' not in hist.GetName():
        pad.SetLogy(hist.logy)


class VisHub(object):

    def __init__(self, *args, **kwargs):
        super(VisHub, self).__init__()
        self.args = args
        self.kwargs = kwargs
        su.gcanvas().Clear()

    def compare_visually(self, hists, loggs=None):
        with plt.style():
            vis = Visualizer(*self.args, **self.kwargs)
            neglimits = any(i < 0 for i in vis.rrange)
            ignoreratio = neglimits and vis.rrange

            if len(hists) != 2 or ignoreratio:
                vis = MultipleVisualizer(*self.args, **self.kwargs)
                return vis.compare_visually(hists, loggs=loggs)

            if len(hists) == 2 and not br.same_binning(hists[0], hists[1]):
                vis = MultipleVisualizer(*self.args, **self.kwargs)
                return vis.compare_visually(hists, loggs=loggs)
            return vis.compare_visually(hists, loggs=loggs)


class MultipleVisualizer(object):
    output_prefix = 'compared-'
    ncolors = 5

    def __init__(self, size, rrange, crange, stop, oname, labels, **kwargs):
        super(MultipleVisualizer, self).__init__()
        self.size = size
        self.cache = []
        self.crange = crange
        self.oname = oname
        self.stop = stop
        self.labels = labels

    def decorate_hist(self, hist, index=0):
        color, marker = self._color_marker(index, hist)
        hist.SetLineColor(color)
        # hist.SetFillColor(color)
        hist.SetMarkerStyle(marker)
        hist.SetMarkerColor(color)
        return hist

    @br.init_inputs
    def compare_visually(self, hists, pad=None, loggs=None, canvas=None):
        if loggs is not None and not self.stop:
            self.cached_hists = hists
            loggs.update({"compare": self})
            return

        canvas = su.gcanvas(size=self.size, resize=True)
        su.ticks(canvas)

        ycenter = 0.6
        ywidth = len(hists) * 0.08
        yend = min(0.9, ycenter + ywidth / 2)
        ystart = max(0.2, ycenter - ywidth / 2)

        legend = ROOT.TLegend(0.55, ystart, 0.9, yend)
        legend.SetBorderSize(0)
        legend.SetFillStyle(0)

        if self.labels:
            for h, l in zip(hists, self.labels):
                h.label = l

        first_hist = next(iter(hists))
        try:
            first_hist.SetStats(False)
        except AttributeError:
            pass

        mainpad = pad if pad else su.gcanvas()
        mainpad.cd()
        set_pad_logx(first_hist, mainpad)
        set_pad_logy(first_hist, mainpad)

        for i, h in enumerate(hists):
            self.decorate_hist(h, index=i)
            if self.crange:
                h.SetAxisRange(self.crange[0], self.crange[1], 'Y')
            h.DrawCopy('colz same ' + h.GetOption())
            legend.AddEntry(h, h.label)

        template = first_hist.Clone("{}_template".format(first_hist.GetName()))
        self._drawable(template, hists)
        # Don't draw legend for TH2 histograms
        if not issubclass(type(first_hist), ROOT.TH2):
            legend.Draw('same')

        ROOT.gStyle.SetOptStat(0)
        self.cache.append(legend)
        if pad:
            return None

        self.io(canvas, hists, loggs)
        # This shouldn't return anything
        # return first_hist

    def _drawable(self, template, hists):
        if issubclass(type(template), ROOT.TH2):
            option = "colz"
            maxbins = max(
                template.GetNbinsX(),
                template.GetNbinsY()
            )
            if maxbins < 20:
                option += " text"
            template.Draw(option)
            return template

        stack = ROOT.THStack("test", template.GetTitle())
        list(map(stack.Add, hists))
        stack.Draw("colz nostack")
        stack.GetXaxis().SetTitle(template.GetXaxis().GetTitle())
        stack.GetYaxis().SetTitle(template.GetYaxis().GetTitle())
        stack.SetMaximum(stack.GetMaximum("nostack") * 1.05)
        stack.SetMinimum(stack.GetMinimum("nostack") * 0.95)
        stack.GetXaxis().SetRangeUser(*calculate_x_limits(hists))
        stack.GetXaxis().SetMoreLogLabels(True)
        self.cache.append(stack)
        self.cache.extend(hists)
        return stack

    def _color_marker(self, i, h):
        color = br.BR_COLORS[i % len(br.BR_COLORS)]
        if h.marker:
            return color, 20 + h.marker

        return color, 20 + i // len(br.BR_COLORS)

    def io(self, canvas, hists, loggs):
        cloned = canvas.Clone()
        cloned.SetName('c' + hists[0].GetName())
        cloned.Write()
        su.wait(stop=self.stop)

    def Write(self):
        return self.compare_visually(self.cached_hists)


class Visualizer(MultipleVisualizer):
    def __init__(self, size, rrange, crange, stop, oname, labels, ratio=""):
        super(Visualizer, self).__init__(
            size, rrange, crange, stop, oname, labels)
        self.rrange = rrange
        self.ratio = ratio

    def _canvas(self, hists):
        c1 = su.gcanvas(size=self.size, resize=True)
        c1.Clear()
        # print(br.chi2ndf(*hists))

        mainpad = ROOT.TPad("mainpad", "main plot", 0, 0.3, 1, 1)
        mainpad.SetBottomMargin(0)
        su.ticks(mainpad)
        mainpad.Draw()
        c1.cd()

        ratiopad = ROOT.TPad("ratiopad", "ratio", 0, 0, 1, 0.3)
        ratiopad.SetTopMargin(0)
        ratiopad.SetBottomMargin(0.2)
        ratiopad.Draw()
        su.ticks(ratiopad)
        return c1, mainpad, ratiopad

    def draw_ratio(self, ratio, pad):
        self.cache.append(ratio)
        pad.cd()
        su.adjust_labels(ratio, ratio, scale=7. / 3)
        ratio.GetYaxis().CenterTitle(True)
        ratio.SetTitle('')
        set_pad_logx(ratio, pad)
        ratio.Draw()

        self.fit_ratio(ratio)
        self.set_ratio_yaxis(ratio)
        self.decorate_hist(ratio)
        return ratio

    def set_ratio_yaxis(self, ratio, n=3):
        bins, _, _, _ = br.bins(ratio)
        try:
            ymin, ymax = self.rrange
            ratio.SetAxisRange(ymin, ymax, 'Y')
            return
            # print(ymin, ymax)
            if any(ymin < b < ymax for b in bins):
                ratio.SetAxisRange(ymin, ymax, 'Y')
                return
        except ValueError:
            pass

        bins, _, _, _ = br.bins(ratio)
        mean, std = np.mean(bins), np.std(bins)
        no_outliers = [b for b in bins if abs(b - mean) < n * std]

        if not no_outliers:
            return

        a, b = min(no_outliers), max(no_outliers)
        ratio.SetAxisRange(a, b, 'Y')

    def _fit(self, ratio):
        # NB: Add fitfunc as an attribute to
        # the numerator histogram to get the output
        ratio.SetStats(True)
        ROOT.gStyle.SetOptStat()
        # ROOT.gStyle.SetOptFit(1011)
        ROOT.gStyle.SetStatFontSize(0.1)
        ROOT.gStyle.SetOptStat('')
        ROOT.gStyle.SetStatX(0.35)
        ROOT.gStyle.SetStatW(0.1)
        ROOT.gStyle.SetStatStyle(0)
        ROOT.gStyle.SetStatBorderSize(0)
        ROOT.gStyle.SetOptFit(1)
        ratio.fitfunc.SetLineColor(ROOT.kBlue + 1)
        ratio.fitfunc.SetMarkerColor(ROOT.kBlue + 1)
        ratio.fitfunc.SetLineWidth(4)
        ratio.Fit(ratio.fitfunc, "Rq")

    def fit_ratio(self, ratio):
        try:
            self._fit(ratio)
        except AttributeError:  # there is no fitfunc defined
            ROOT.gStyle.SetOptFit(0)
            ROOT.gStyle.SetOptStat(0)
            ratio.SetStats(False)
            return

    @br.init_inputs
    def compare_visually(self, hists, loggs=None):
        a, b = hists
        ratio = br.ratio(a, b, self.ratio)
        br.setp(ratio)
        if loggs is not None and not self.stop:
            self.cached_ratio = ratio
            self.cached_hists = hists
            loggs.update({"ratio": self})
            return ratio
        return self.compare_show_ratio(hists, ratio)

    def compare_show_ratio(self, hists, ratio, loggs=None):
        canvas, mainpad, ratiopad = self._canvas(hists)
        super(Visualizer, self).compare_visually(hists, mainpad)
        ratio = self.draw_ratio(ratio, ratiopad)
        # ctrl+alt+f4 closes enire canvas not just a pad.
        canvas.Update()
        ratiopad.Update()
        canvas.cd()
        self.io(canvas, hists, loggs)
        return su.adjust_labels(ratio, hists[0])

    def Write(self):
        return self.compare_show_ratio(
            self.cached_hists,
            self.cached_ratio)
