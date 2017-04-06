#!/usr/bin/python

import sys
import ROOT
import json

from badmap import badmap
ROOT.TH1.AddDirectory(False)

def define_colors(ci = 1000):
    colors = [ (219 , 86  , 178), (160 , 86  , 219), (86  , 111 , 219), (86  , 211 , 219), (86  , 219 , 127),  (219 , 194 , 86), (219 , 94 , 86)][::-1]
    rcolors = [[b / 255. for b in c] for c in colors]
    rcolors = [ROOT.TColor(ci + i, *color) for i, color in enumerate(rcolors)]
    return ci, rcolors

class Styler(object):
    ci, colors = define_colors()

    def __init__(self, filename):
        super(Styler, self).__init__()
        with open(filename) as f:
            self.data = json.load(f)
        self.hists, self.hitmap = self.read_data()

        
    def read_data(self):
        hists, hitmap = None, None

        if 'histograms' in self.data:
            hists = self.data['histograms']
            self.histograms = [self.read_histogram(h, hists[h]) for h in hists] 

        if 'hitmap' in self.data:
            hitmap = [[self.read_histogram(h % i, self.data["hitmap"][h]) for i in range(1, 5)] for h in sorted(self.data['hitmap'])] 
        return hists, hitmap


    def read_histogram(self, path, properties):
        # Extract root file
        filename, path = path.split('.root/')
        path = path.split('/')

        # Extract list name 
        lst, path = path[0], path[1:]
        infile = ROOT.TFile(filename + '.root')

        # Handle situation when we have nested lists
        obj = infile.Get(lst)
        for n in path:
            obj = obj.FindObject(n)

        assert obj, 'Specify right path to histogram. ' + lst + ' Current path: ' + path + '. Or check your .root file.'

        if 'projecty' in properties: 
            obj = obj.ProjectionY(obj.GetName() + '_y', obj.GetXaxis().FindBin(properties['projecty']), -1)

        if 'projectx' in properties: 
            obj = obj.ProjectionX(obj.GetName() + '_x', obj.GetYaxis().FindBin(properties['projectx']), -1)

        obj.SetStats(False)
        obj.oname = properties['oname'] if 'oname' in properties else ''
        obj.label = properties['label'] if 'label' in properties else ''
        obj.option = properties['option'] if 'option' in properties else ''
        
        if 'label' in properties: obj.label = properties['label']
        if 'color' in properties: obj.SetLineColor(properties['color'])
        if 'color' in properties: obj.SetMarkerColor(properties['color'])
        if 'title' in properties: obj.SetTitle(properties['title'])
        if 'rebin' in properties: obj.Rebin(properties['rebin'])
        if 'stats' in properties: 
            obj.SetStats(True)
            ROOT.gStyle.SetOptStat(properties['stats'])
        if 'option' in properties: obj.SetOption(properties['option'])
        if 'normalize' in properties: 
            obj.Scale( properties['normalize'] / obj.Integral() )
        if 'yprecision' in properties:
            obj.GetYaxis().SetTitle(obj.GetYaxis().GetTitle() + properties['yprecision'] % obj.GetBinWidth(1))
        if 'markerstyle' in properties: obj.SetMarkerStyle(properties['markerstyle'])
        if 'fillcolor' in properties: obj.SetFillColor(properties['fillcolor'])
        if 'fillstyle' in properties: obj.SetFillStyle(properties['fillstyle'])
        if 'linewidth' in properties: obj.SetLineWidth(properties['linewidth'])
        if 'ratio' in properties: obj.ratio = properties['ratio']

        if 'fitrange' in properties:
            self.fit_simple(obj, properties)
        return obj


    def fit_simple(self, obj, properties):
        fitrange = properties['fitrange']
        fitfunc = properties['fitfunc']
        fitpars = properties['fitpars']
        function = ROOT.TF1('hTest', fitfunc, *fitrange)
        function.SetLineColor(46)
        function.SetParameters(*fitpars)
        ROOT.gStyle.SetOptFit()
        obj.Fit('hTest')


    def ratioplot(self, canvas):
        if not len(self.histograms) == 2:
            return

        attributes = sum(map(dir, self.histograms), [])

        if not 'ratio' in sum(map(dir, self.histograms), []):
            return

        num, denom = sorted(self.histograms, key=lambda x: x.ratio)
        ratio = num.Clone(num.GetName() + '_ratio')
        ratio.Divide(denom)
        ratio.SetTitle('')
        canvas.cd()
        ratio.Draw()
        canvas.Update()
        return ratio

    def form_ratio_plot(self, hists, canvas, props):

        if len(hists) != 2: 
            return canvas, canvas, canvas 

        pad1 = ROOT.TPad("pad1", "main plot", 0, 0.3, 1, 1);
        pad1.SetBottomMargin(0);
        pad1.Draw()
        canvas.cd()
        pad2 = ROOT.TPad("pad2", "ratio", 0, 0, 1, 0.3);
        pad2.SetTopMargin(0);
        pad2.SetBottomMargin(0.2);
        pad2.Draw();
        self.decorate_pad(pad2, props)
        return canvas, pad1, pad2


    def draw(self):
        if not self.hists:
            return

        props = self.data['canvas']
        size = props['size']
        canvas = ROOT.TCanvas('c1', 'c1', 128 * size, 96 * size)
        canvas, mainpad, ratio = self.form_ratio_plot(self.histograms, canvas, props)

        mainpad.cd()
        map(lambda x: x.Draw('same'), self.histograms)
        legend = self.decorate_legend(self.histograms, props)
        
        self.decorate_pad(mainpad, props)
        if 'output' in props:
            mainpad.SaveAs(props['output'])

        mainpad.Update()
        ratio = self.ratioplot(ratio)
        raw_input()


    def drawmap(self):
        size = self.data['canvas']['size']
        canvas = ROOT.TCanvas('c1', 'c1', 128 * size, 96 * size)
        c1 = ROOT.TCanvas('c1', 'c1', 128 * 5, 96 * 5); 
        c1.Divide(2, 2)
        for maps in self.hitmap:
            badmap(maps, c1)
        self.decorate_map(c1)
        raw_input()

    def decorate_map(self, canvas):
        if not 'canvas' in self.data:
            return

        props = self.data['canvas']

        canvas.cd(1)
        legend = self.decorate_legend(zip(*self.hitmap)[0], props)

        for i in range(4): self.decorate_pad(canvas.cd(i + 1), props)

        canvas.Update()
        canvas.SaveAs(props['output'])

    def decorate_pad(self, pad, props):
        ROOT.gPad.SetTickx()
        ROOT.gPad.SetTicky() 

        if 'logy' in props: pad.SetLogy(props['logy'])
        if 'logx' in props: pad.SetLogx(props['logx'])
        if 'gridx' in props: pad.SetGridx()
        if 'gridy' in props: pad.SetGridy()

    def decorate_legend(self, hists, props):
        if not 'legend' in props:
            return 

        legend = ROOT.TLegend(*props['legend'])
        legend.SetFillStyle(0)
        legend.SetBorderSize(0)
        map(lambda x: legend.AddEntry(x, x.label), hists)
        legend.Draw()
        return legend



def main():
    assert len(sys.argv) == 2, "Usage: style.py rules.json"
    s = Styler(sys.argv[1])
    s.draw()
    s.drawmap()

if __name__ == '__main__':
    main()