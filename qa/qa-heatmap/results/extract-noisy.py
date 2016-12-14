#!/usr/bin/python2

import ROOT

class ExctractNoisy(object):
    def __init__(self, filename, function, name):
        super(ExctractNoisy, self).__init__()
        self.modules = self.read(filename, function, name)
        self.cells = [[]]

    def noisy_cells(self, hists, threshold):
        return [[[x, z, i + 1] for x in range(h.GetNbinsX()) for z in range(h.GetNbinsY()) if h.GetBinContent(x + 1, z + 1) > threshold] for i, h in enumerate(hists)]

    def inspect(self, threshold = 2000):
        self.cells = self.noisy_cells(self.modules, threshold)
        for h, cells in zip(self.modules, self.cells):
            for cell in cells: h.SetBinContent(cell[0] + 1, cell[1] + 1, 0)
            # h.Draw('lego')
            # ROOT.gROOT.FindObject('c1').Update()
            # raw_input('')

    def read(self, filename, function, name):
        inlist = function(ROOT.TFile(filename))
        histograms = [inlist.FindObject(name % i) for i in range(1, 5)]
        return histograms

    def save(self, ofilename, oname):
        ofile = ROOT.TFile(ofilename, 'recreate')

        outhists = [h.Clone(oname % (i + 1)) for i, h in enumerate(self.modules)]
        for h, cells in zip(outhists, self.cells):
            h.Reset()
            for cell in cells: h.SetBinContent(cell[0] + 1, cell[1] + 1, 1)
            # h.Write()

        ofile.Write()
        ofile.Close()


def main():
    extractor = ExctractNoisy('LHC16k-pass1-half-almost-clean.root', lambda x: x.PhysTender, 'hCluNXZM%d_0')
    extractor.inspect(2000)
    extractor.save('very-noisy-cells-LHC16k.root', 'PHOS_BadMap_mod%d')

if __name__ == '__main__':
    main()