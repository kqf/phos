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
        if 'stats' in properties: obj.SetStats(True)
        if 'option' in properties: obj.SetOption(properties['option'])
        if 'normalize' in properties: 
            obj.Scale( properties['normalize'] / obj.Integral() )
        if 'yprecision' in properties:
            obj.GetYaxis().SetTitle(obj.GetYaxis().GetTitle() + properties['yprecision'] % obj.GetBinWidth(1))
            
        # TODO: Add markers, fillcolors, width, etc.


        return obj

    def draw(self):
        if not self.hists:
            return

        props = self.data['canvas']
        size = props['size']
        canvas = ROOT.TCanvas('c1', 'c1', 128 * size, 96 * size)

        map(lambda x: x.Draw('same'), self.histograms)
        legend = self.decorate_legend(self.histograms, props)
        
        self.decorate_pad(canvas, props)
        canvas.Draw()
        if 'output' in props: canvas.SaveAs(props['output'])
        raw_input()

    def drawmap(self, name):
        c1 = ROOT.TCanvas(name, name, 128 * 5, 96 * 5); 
        c1.Divide(2, 2)
        for maps in self.hitmap:
            badmap(maps, c1)
        self.decorate_map(c1)
        raw_input()

    def decorate_map(self, canvas):
        if not 'canvas_per_module' in self.data:
            return

        props = self.data['canvas_per_module']

        canvas.cd(1)
        legend = self.decorate_legend(zip(*self.hitmap)[0], props)

        for i in range(4): self.decorate_pad(canvas.cd(i + 1), props)

        canvas.Update()
        canvas.SaveAs(props['output'])
        raw_input()

    def decorate_pad(self, pad, props):
        ROOT.gStyle.SetOptStat(0)
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
    s.drawmap('hitmap')

if __name__ == '__main__':
    main()