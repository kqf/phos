#!/usr/bin/python2

import ROOT
import json
from sutils import wait, get_canvas, Cc, adjust_canvas, adjust_labels
import numpy as np

class Visualizer(object):
    def __init__(self, size, rrange, ratiofit):
        super(Visualizer, self).__init__()
        self.size = size
        self.cache = []
        self.rrange = rrange
        self.ratiofit = ratiofit
        self.output_prefix = 'compared-'
        

    def preare_ratio_plot(self, hists, canvas):
        c1 = canvas if canvas else get_canvas(*self.size)
        c1.Clear()
        if len(hists) != 2: return c1, c1, c1
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
        return c1, pad1, pad2

    @staticmethod
    def ratio(hists):
        if len(hists) != 2: return
        a, b = hists
        ratio = a.Clone('ratio' + a.GetName())
        if 'fitfunc' in dir(a):
            ratio.fitfunc = a.fitfunc

        # Enable binomail errors
        ratio.Divide(a, b, 1, 1, "B")
        label = a.label + ' / ' + b.label
        ratio.SetTitle('')
        ratio.GetYaxis().SetTitle(label)
        return ratio

    def draw_ratio(self, hists):
        ratio = self.ratio(hists)
        if not ratio:
            return

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
        # TODO: avoid numpy?
        mean, std = np.mean(bins), np.std(bins)
        withoutoutliers = [b for b in bins if abs(b - mean) < n * std]

        if not withoutoutliers:
            return

        a, b = map(lambda x: x(withoutoutliers), (min, max))
        ratio.SetAxisRange(a, b , 'Y')


    def linear_fit(self, ratio):
        if not self.ratiofit:
            return False

        ratio.Fit("pol1", "q", "", *self.ratiofit)
        func = ratio.GetFunction("pol1")
        func.SetLineColor(38)
        return True

    def nonlinear_fit(self, ratio):
        if not 'fitfunc' in dir(ratio):
            return False

        ratio.Fit(ratio.fitfunc, "r")
        ratio.fitfunc.SetLineColor(38)
        return True
    
    def fit_ratio(self, ratio):
        if not (self.linear_fit(ratio) or self.nonlinear_fit(ratio)):
            return

        ratio.SetStats(True)
        ROOT.gStyle.SetStatFontSize(0.1)
        ROOT.gStyle.SetOptStat('')
        ROOT.gStyle.SetStatX(0.35)
        ROOT.gStyle.SetStatW(0.1)
        ROOT.gStyle.SetStatStyle(0)
        ROOT.gStyle.SetStatBorderSize(0)
        ROOT.gStyle.SetOptFit(1)


    def prepare_hists(self, hists):
        for h in hists:
            if not 'priority' in dir(h):
                h.priority = 999


    def compare_visually(self, hists, ci, stop = True, canvas = None):
        self.prepare_hists(hists)
        canvas, mainpad, ratiopad = self.preare_ratio_plot(hists, canvas)

        if len(hists) == 1:
            adjust_canvas(canvas)

        legend = ROOT.TLegend(0.7, 0.4, 0.8, 0.6)
        legend.SetBorderSize(0)
        legend.SetFillStyle(0)
        legend.SetTextSize(0.04)

        mainpad.cd()
        mainpad.SetGridx()
        mainpad.SetGridy()

        first_hist = sorted(hists, key=lambda x: x.priority)[0]
        first_hist.SetStats(False)
        first_hist.DrawCopy()
        for i, h in enumerate(hists): 
            h.SetStats(False)
            h.SetLineColor(ci + i)
            h.SetFillColor(ci + i)
            h.SetMarkerStyle(20)
            h.SetMarkerColor(ci + i)
            h.DrawCopy('same')
            legend.AddEntry(h, h.label)

        legend.Draw('same')

        if 'spectr' in first_hist.GetName() or 'logy' in dir(first_hist):
            ROOT.gPad.SetLogy()

        # ROOT.gStyle.SetOptStat(0)
        mainpad.SetTickx()
        mainpad.SetTicky() 

        ratiopad.cd()
        ratio = self.draw_ratio(hists)

        # ctrl+alt+f4 closes enire canvas not just a pad.
        canvas.cd()

        if stop:
            fname = hists[0].GetName() + '-' + '-'.join(x.label for x in hists) 
            wait(self.output_prefix + fname.lower(), save=True)

        self.cache.append(ratio)
        self.cache.append(legend)
        return adjust_labels(ratio, hists[0])

        
    def compare_multiple(self, hists, ci):
        canvas = get_canvas(*self.size)
        canvas.Clear()
        canvas.Divide(2, 2)

        hists = zip(*hists)

        for h in hists:
            print h

        for i, h in enumerate(hists):
            self.compare_visually(h, ci, False, canvas.cd(i + 1))

        canvas.cd()
        wait(self.output_prefix + hists[0][0].GetName(), True)

def define_colors(ci = 1000):
    with open("config/colors.json") as f:
        conf = json.load(f)
        
    colors = conf["colors"][::-1]
    rcolors = [[b / 255. for b in c] for c in colors]
    rcolors = [ROOT.TColor(ci + i, *color) for i, color in enumerate(rcolors)]
    return ci, rcolors

class Comparator(object):
    ci, colors = define_colors()

    def __init__(self, size = (1, 1), rrange = None, ratiofit = False):
        super(Comparator, self).__init__()
        self.vi = Visualizer(size, rrange, ratiofit)


    def compare_multiple_ratios(self, hists, baselines, compare = None):
        if not compare:
            compare = self.vi.compare_visually

        def ratio(a, b):
            h = a.Clone(a.GetName() + '_ratio')
            # Here we assume that a, b have the same lables
            h.label = a.label
            h.Divide(b)
            ytitle = lambda x: x.GetYaxis().GetTitle()
            h.SetTitle(a.GetTitle() + ' / ' + b.GetTitle())
            h.GetYaxis().SetTitle(ytitle(a) +  ' / ' + ytitle(b))
            return h

        compare(map(ratio, hists, baselines), self.ci)



    def compare_ratios(self, hists, baseline, compare = None):
        if not compare:
            compare = self.vi.compare_visually

        def ratio(a):
            h = a.Clone(a.GetName() + '_ratio')
            h.label = a.label + '/' + baseline.label
            h.Divide(baseline)
            return h

        compare(map(ratio, hists), self.ci)


    def compare_set_of_histograms(self, l, compare = None):
        if not compare:
            compare = self.vi.compare_visually

        result = [compare(hists, self.ci) for hists in zip(*l)]
        return result


    def compare_lists_of_histograms(self, l1, l2, ignore = [], compare = None):
        if len(l1) != len(l2): 
            print Cc.fail('Warning files have different size')

        if not compare:
            compare = self.vi.compare_visually

        for h in l1: 
            candidate = self.find_similar_in(l2, h)
            if not candidate or candidate.GetName() in ignore: continue
            compare(h, candidate, self.ci)

        print "That's it!! Your computation is done"


    def compare_multiple(self, l):
        for hists in zip(*l):
            self.vi.compare_multiple(hists, self.ci)

    @staticmethod
    def find_similar_in(self, lst, ref):
        candidates = [h for h in lst if h.GetName() == ref.GetName() ]
        if not candidates:
            print Cc.warning('Warning: There is no such histogram ') + Cc.ok(ref.GetName()) + Cc.warning(' in the second file or it\'s empty')
            return None
        if len(candidates) > 1: print Cc.warning('Warning: you have multiple histograms with the same name!!! Act!!')
        return candidates[0]
        
def main():
    print "Use:\n\t... \n\tcmp = Comparator((0.5, 2))\n\t...\n\nto compare lists of histograms."

if __name__ == '__main__':
    main()
