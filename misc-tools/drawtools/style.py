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

        assert obj, 'Specify right path to histogram. Current path: ' + path

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
        return obj

    def draw(self):
        if not self.hists:
            return

        props = self.data['canvas']
        size = props['size']
        canvas = ROOT.TCanvas('c1', 'c1', 128 * size, 96 * size)

        map(lambda x: x.Draw('same'), self.histograms)

        ROOT.gStyle.SetOptStat(0)
        ROOT.gPad.SetTickx()
        ROOT.gPad.SetTicky() 

        legend = ROOT.TLegend(*props['legend'])
        map(lambda x: legend.AddEntry(x, x.label), self.histograms)
        legend.Draw('same')
        legend.SetBorderSize(0)
        legend.SetFillStyle(0)
        # legend.SetTextSize(0.04)

        canvas.SetLogy(props['logy'])
        canvas.SetGridx(props['gridx'])
        canvas.Draw()
        canvas.SaveAs(props['output'])
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

        if 'legend' in props:
            legend = ROOT.TLegend(*props['legend'])
            legend.SetFillStyle(0)
            legend.SetBorderSize(0)
            map(lambda x: legend.AddEntry(x, x.label), zip(*self.hitmap)[0])
            canvas.cd(1)
            legend.Draw()

        for i in range(4): 
            pad = canvas.cd(i + 1)
            if 'logy' in props: pad.SetLogy()
            if 'logx' in props: pad.SetLogx()
            if 'gridx' in props: pad.SetGridx()
            if 'gridy' in props: pad.SetGridy()

        canvas.Update()
        canvas.SaveAs(props['output'])
        raw_input()




def main():
    assert len(sys.argv) == 2, "Usage: style.py rules.json"
    s = Styler(sys.argv[1])
    s.draw()
    s.drawmap('hitmap')

if __name__ == '__main__':
    main()