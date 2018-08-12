import ROOT
import numpy as np

from broot import BROOT as br
import sutils as su


def info(hist):
    pave = ROOT.TPaveText(.3, .6, .4, .8, "NBNDC")
    pave.AddText("ALICE, PHOS")
    pave.AddText("pp at #sqrt{s}=13 TeV")
    pave.SetFillStyle(0)
    pave.SetLineColor(0)
    # pave.SetTextSize(12)
    pave.Draw()
    return pave


def set_pad_logx(hist, pad):
    if 'eff' in hist.GetName().lower():
        return

    if hist.logx:
        pad.SetLogx(hist.logx)
        hist.GetXaxis().SetMoreLogLabels(hist.logx)
        return

    # Draw logx for increasing bin width
    start_width = hist.GetBinWidth(1)
    stop_width = hist.GetBinWidth(hist.GetNbinsX() - 1)
    pad.SetLogx(start_width < stop_width)
    hist.GetXaxis().SetMoreLogLabels()

    if hist.GetName() == 'testtest':
        print hist, start_width < stop_width


class VisHub(object):

    def __init__(self, *args, **kwargs):
        super(VisHub, self).__init__()
        self._double = Visualizer(*args, **kwargs)
        self._regular = MultipleVisualizer(*args, **kwargs)
        su.gcanvas().Clear()

    def compare_visually(self, hists, ci):
        neglimits = any(i < 0 for i in self._double.rrange)
        ignoreratio = neglimits and self._double.rrange

        if len(hists) != 2 or ignoreratio:
            return self._regular.compare_visually(hists, ci)
        return self._double.compare_visually(hists, ci)


class MultipleVisualizer(object):
    output_prefix = 'compared-'
    ncolors = 5

    def __init__(self, size, rrange, crange, stop, oname, labels, loggs):
        super(MultipleVisualizer, self).__init__()
        self.size = size
        self.cache = []
        self.crange = crange
        self.oname = oname
        self.stop = stop
        self.labels = labels
        self.loggs = loggs

    @br.init_inputs
    def compare_visually(self, hists, ci, pad=None):
        canvas = su.gcanvas(self.size[0], self.size[1], resize=True)
        su.ticks(canvas)
        legend = ROOT.TLegend(0.55, 0.65, 0.8, 0.85)
        legend.SetBorderSize(0)
        legend.SetFillStyle(0)
        legend.SetTextSize(0.04)
        # legend.SetTextFont(132)

        if self.labels:
            for h, l in zip(hists, self.labels):
                h.label = l

        first_hist = sorted(hists, key=lambda x: x.priority)[0]
        try:
            first_hist.SetStats(False)
        except AttributeError:
            pass

        mainpad = pad if pad else su.gcanvas()
        mainpad.cd()
        set_pad_logx(first_hist, mainpad)
        if 'eff' not in first_hist.GetName():
            mainpad.SetLogy(first_hist.logy)

        for i, h in enumerate(hists):
            color, marker = self._color_marker(ci, i, h)
            h.SetLineColor(color)
            h.SetFillColor(color)
            h.SetMarkerStyle(marker)
            h.SetMarkerColor(color)
            if self.crange:
                h.SetAxisRange(self.crange[0], self.crange[1], 'Y')
            h.DrawCopy('colz same ' + h.GetOption())
            legend.AddEntry(h, h.label)

        self._drawable(first_hist, hists)
        # Don't draw legend for TH2 histograms
        if not issubclass(type(first_hist), ROOT.TH2):
            legend.Draw('same')

        ROOT.gStyle.SetOptStat(0)
        self.cache.append(legend)
        if pad:
            return None

        fname = hists[0].GetName() + '-' + '-'.join(x.label for x in hists)
        oname = self._oname(fname.lower())
        self.io(canvas, hists, oname)
        return None

    def _drawable(self, first_hist, hists):
        if issubclass(type(first_hist), ROOT.TH2):
            option = "colz"
            maxbins = max(
                first_hist.GetNbinsX(),
                first_hist.GetNbinsY()
            )
            if maxbins < 20:
                option += " text"
            first_hist.Draw(option)
            return first_hist

        stack = ROOT.THStack("test", first_hist.GetTitle())
        map(stack.Add, hists)
        stack.Draw("colz nostack")
        stack.GetXaxis().SetTitle(first_hist.GetXaxis().GetTitle())
        stack.GetYaxis().SetTitle(first_hist.GetYaxis().GetTitle())
        stack.SetMaximum(stack.GetMaximum("nostack") * 1.05)
        stack.SetMinimum(stack.GetMinimum("nostack") * 0.95)
        stack.GetXaxis().SetRangeUser(*br.hist_range(first_hist))
        stack.GetXaxis().SetMoreLogLabels(
            first_hist.GetXaxis().GetMoreLogLabels()
        )
        self.cache.append(stack)
        self.cache.extend(hists)
        return stack

    def _color_marker(self, ci, i, h):
        color = ci + i % self.ncolors
        if h.marker:
            return color, 20 + h.marker

        return color, 20 + i // self.ncolors

    def _oname(self, name):
        if self.oname:
            return self.oname

        oname = self.output_prefix + name
        return oname

    def io(self, canvas, hists, oname):
        cloned = canvas.Clone()
        cloned.SetName('c' + hists[0].GetName())

        if self.loggs:
            self.loggs.update('compare', cloned)
        else:
            su.save_canvas(oname, pdf=False)

        if not self.loggs and self.stop:
            su.wait(oname, save=True, draw=self.stop)


class Visualizer(MultipleVisualizer):
    def __init__(self, size, rrange, crange, stop, oname, labels, loggs):
        super(Visualizer, self).__init__(
            size, rrange, crange, stop, oname, labels, loggs)
        self.rrange = rrange

    def _canvas(self, hists):
        c1 = su.gcanvas(self.size[0], self.size[1], resize=True)
        c1.Clear()
        # print br.chi2ndf(*hists)

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

    def draw_ratio(self, hists, pad):
        a, b = hists
        ratio = br.ratio(a, b)
        self.cache.append(ratio)

        pad.cd()
        su.adjust_labels(ratio, hists[0], scale=7. / 3)
        ratio.GetYaxis().CenterTitle(True)
        ratio.SetTitle('')
        set_pad_logx(ratio, pad)
        ratio.Draw()

        self.fit_ratio(ratio)
        self.set_ratio_yaxis(ratio)
        return ratio

    def set_ratio_yaxis(self, ratio, n=3):
        bins, _, _ = br.bins(ratio)
        try:
            ymin, ymax = self.rrange
            ratio.SetAxisRange(ymin, ymax, 'Y')
            return
            # print ymin, ymax
            if any(ymin < b < ymax for b in bins):
                ratio.SetAxisRange(ymin, ymax, 'Y')
                return
        except ValueError:
            pass

        bins, _, _ = br.bins(ratio)
        mean, std = np.mean(bins), np.std(bins)
        no_outliers = [b for b in bins if abs(b - mean) < n * std]

        if not no_outliers:
            return

        a, b = min(no_outliers), max(no_outliers)
        ratio.SetAxisRange(a, b, 'Y')

    def _fit(self, ratio):
        # NB: Add fitfunc as an attribute to
        # the numerator histogram to get the output
        ratio.Fit(ratio.fitfunc, "Rq")
        ratio.fitfunc.SetLineColor(38)
        ratio.SetStats(True)

    def fit_ratio(self, ratio):
        try:
            self._fit(ratio)
        except AttributeError:  # there is no fitfunc defined
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
        oname = self._oname(fname.lower())
        self.io(canvas, hists, oname)
        return su.adjust_labels(ratio, hists[0])
