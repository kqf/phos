#!/usr/bin/python

import sys
import ROOT
import json

class Styler(object):
    def __init__(self, filename):
        super(Styler, self).__init__()
        with open(filename) as f:
            self.data = json.load(f)
        hists = self.data['histograms']
        self.histograms = [self.read_histogram(h.split('/'), hists[h]) for h in hists] 

    def read_histogram(self, path, properties):
        filename, lst, path = path[0], path[1], path[2:]
        infile = ROOT.TFile(filename)

        obj = infile.Get(lst)
        for n in path:
            obj = obj.FindObject(n)

        assert obj, 'Specify right path to histogram. Current path: ' + path

        obj.label = properties['label']
        obj.SetLineColor(properties['color'])
        obj.SetMarkerColor(properties['color'])
        obj.SetTitle(properties['title'])
        if properties['normalize']: obj.Scale( properties['normalize'] / obj.Integral() )
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

def main():
    assert len(sys.argv) == 2, "Usage: style.py rules.json"
    s = Styler(sys.argv[1])
    s.draw()

if __name__ == '__main__':
    main()