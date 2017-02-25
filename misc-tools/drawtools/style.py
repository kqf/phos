#!/usr/bin/python

import sys
import ROOT
import json

from badmap import badmap
ROOT.TH1.AddDirectory(False)

class Styler(object):
    def __init__(self, filename):
        super(Styler, self).__init__()
        with open(filename) as f:
            self.data = json.load(f)
        hists = self.data['histograms']
        self.histograms = [self.read_histogram(h.split('/'), hists[h]) for h in hists] 
        self.hitmap = [[self.read_histogram((h % i).split('/'), self.data["hitmap"][h]) for i in range(1, 5)] for h in sorted(self.data['hitmap'])] 

    def read_histogram(self, path, properties):
        filename, lst, path = path[0], path[1], path[2:]
        infile = ROOT.TFile(filename)

        obj = infile.Get(lst)
        for n in path:
            obj = obj.FindObject(n)

        assert obj, 'Specify right path to histogram. Current path: ' + path

        if 'projecty' in properties: 
            obj = obj.ProjectionY(obj.GetName() + '_y', obj.GetXaxis().FindBin(properties['projecty']), -1)

        print obj.GetName(), obj.GetEntries()

        if 'label' in properties: obj.label = properties['label']
        if 'color' in properties: obj.SetLineColor(properties['color'])
        if 'color' in properties: obj.SetMarkerColor(properties['color'])
        if 'title' in properties: obj.SetTitle(properties['title'])
        if 'rebin' in properties: obj.Rebin(properties['rebin'])
        if 'option' in properties: 
            obj.SetOption(properties['option'])
            obj.option = properties['option']
        if 'normalize' in properties: 
            obj.Scale( properties['normalize'] / obj.Integral() )
        return obj

    def draw(self):
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

    def draw(self):
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
            print maps
            badmap(maps, c1)

        props = self.data['canvas']
        legend = ROOT.TLegend(*props['legend'])
        map(lambda x: legend.AddEntry(x, x.label), zip(*self.hitmap)[0])
        c1.cd(1)
        legend.Draw()
        for i in range(4): 
            pad = c1.cd(i + 1)
            pad.SetLogy()
            pad.SetGridx()
            pad.SetGridy()
            
        c1.Update()
        c1.SaveAs('multiple.pdf')

        raw_input()



def main():
    assert len(sys.argv) == 2, "Usage: style.py rules.json"
    s = Styler(sys.argv[1])
    s.draw()
    s.drawmap('hitmap')

if __name__ == '__main__':
    main()