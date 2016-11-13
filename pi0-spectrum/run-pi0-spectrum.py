#!/usr/bin/python

import ROOT

from spectrum.spectrum import PtAnalyzer, Spectrum

def main():
    canvas = ROOT.TCanvas('c1', 'Canvas', 1000, 500)
    mfile = ROOT.TFile('input-data/LHC16k.root')

    second = Spectrum(mfile.PhysNoTender, label = 'Mixing', mode='q').evaluate()
    first  = PtAnalyzer(mfile.PhysNoTender, label = 'No Mixing', mode='q').quantities()

    import spectrum.comparator as cmpr
    diff = cmpr.Comparator()
    diff.compare_lists_of_histograms(first, second)


if __name__ == '__main__':
    main()