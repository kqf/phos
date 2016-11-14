#!/usr/bin/python

import ROOT
import sys

print sys.argv[1]

class NNL2ROOT(object):
    def __init__(self, fname, scale = 1):
        super(NNL2ROOT, self).__init__()
        self.scale = scale = 1 
        self.data, self.sqrts = self.read(fname)
        self.graph()


    def read(self, fname):
        with open(fname, 'r') as ff:
            f = ff.readlines()
            lines = (l for l in f if '*****' in l)
            data = [[float(token) for token in line.split() if '.' in token] for line in lines]
            sqrts = float([l for l in f if 'square root of' in l][0].split()[4])
            for i in f: print i

        return data, sqrts


    def graph(self):
        graph = ROOT.TGraph()
        graph.SetName('nll')
        for i, (pt, sig) in enumerate(self.data): graph.SetPoint(i, pt, sig * self.scale)
        graph.SetTitle('NNL theoretical curve #sqrt{s} = %0.2g TeV' %  (self.sqrts ) + '; P_{t}, GeV/c')
        return graph


    def draw(self):
        graph = self.graph()
        graph.SetMarkerStyle(20)
        graph.SetMarkerColor(47)
        graph.Draw('APL')
        ROOT.gPad.SetLogy()
        raw_input('...')

    def save(self, filename):
        ofile = ROOT.TFile(filename, 'recreate')
        graph = self.graph()
        graph.Write('nnl')
        ofile.Write()


def main():
    if len(sys.argv) < 2: print 'Please, specify the input file.'
    reader = NNL2ROOT(sys.argv[1])
    # When it will be clear what is the scale then
    # All the parameters can be hardcoded.
    # reader = NNL2ROOT(sys.argv[1],  1. / 74. / 1e6 * 1e3)
    reader.save('nnl.root')

if __name__ == '__main__':
    main()