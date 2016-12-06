#!/usr/bin/python

import ROOT
import sys

print sys.argv[1]

class NNL2ROOT(object):
    def __init__(self, fname, scale = 1):
        super(NNL2ROOT, self).__init__()
        self.scale = scale
        self.data, self.sqrts, self.factor = self.read(fname)


    def read(self, fname):
        with open(fname, 'r') as ff:
            f = ff.readlines()
            lines = (l for l in f if '*****' in l)
            data = [[float(token) for token in line.split() if '.' in token] for line in lines]
            sqrts = int(float([l for l in f if 'square root of' in l][0].split()[4]))
            # Initial factorisation scale
            factor = float([l for l in f if 'FACTO SCALE**2' in l][0].split('=')[1].split()[0]) ** 0.5

        return data, sqrts, factor

    def graph(self):
        graph = ROOT.TGraph()
        graph.SetName('nnl')
        for i, (pt, sig) in enumerate(self.data): graph.SetPoint(i, pt, sig * self.scale)
        graph.SetTitle('NNL theoretical curve #sqrt{s} = %0.2g TeV | scale %0.2g' %  (self.sqrts / 1000., self.factor) +  '; P_{t}, GeV/c; #sigma_{fb} #sigma_{#gamma direct}, fb')
        return graph

    def histogram(self):
        # The histogram parameters below should be modified according to bin centers
        # that are listed conf file for nnl calculation .
        hist = ROOT.TH1D('hnnl', 'NNL theoretical curve #sqrt{s} = %0.2g TeV | scale %0.2g' %  (self.sqrts / 1000, self.factor) + '; P_{t}, GeV/c; #sigma_{fb} #sigma_{#gamma direct}, fb', 400, 0, 40)
        hist.Rebin(16)
        # hist.Sumw2()
        for pt, sig in self.data: hist.Fill(pt, sig * self.scale)
        for i in range(hist.GetNbinsX()): hist.SetBinError(i + 1, 0)
        return hist

    def draw(self):
        graph = self.graph()
        graph.SetMarkerStyle(20)
        graph.SetMarkerColor(47)
        graph.Draw('APL')
        ROOT.gPad.SetLogy()
        raw_input('...')

    def save(self, filename):
        hist, graph = self.histogram(), self.graph() 
        ofile = ROOT.TFile(filename, 'recreate')
        hist.Write()
        graph.Write()
        ofile.Write()


def main():
    if len(sys.argv) < 2: print 'Please, specify the input file.'
    # Default values are given in pb ~ 1e12b but we need mb ~ 1e3b.
    reader = NNL2ROOT(sys.argv[1])
    reader.save(sys.argv[1].replace('.out', '') + '.root')

if __name__ == '__main__':
    main()