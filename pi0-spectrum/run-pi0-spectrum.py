#!/usr/bin/python

import ROOT

from spectrum.spectrum import PtAnalyzer

def main():
    canvas = ROOT.TCanvas('c1', 'Canvas', 1000, 500)
    mfile = ROOT.TFile('input-data/LHC16k.root')

    second = PtAnalyzer(mfile.PhysNoTender, label = 'Mixing').quantities()
    first  = PtAnalyzer(mfile.PhysNoTender, label = 'No Mixing').quantities()

    import spectrum.comparator as cmpr
    diff = cmpr.Comparator()
    diff.compare_lists_of_histograms(first, second)


if __name__ == '__main__':
    main()