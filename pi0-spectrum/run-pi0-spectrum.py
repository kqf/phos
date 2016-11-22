#!/usr/bin/python

import ROOT

from spectrum.spectrum import PtAnalyzer, Spectrum

def my_input(filename):
    lst = ROOT.TFile(filename).PhysNoTender
    nevents = lst.FindObject('TotalEvents').GetEntries()
    rawhist = lst.FindObject('hMassPtN3')
    rawmix = lst.FindObject('hMixMassPtN3')
    return [nevents, rawhist, rawmix]

def example_input(filename):
    lst = ROOT.TFile(filename).Data
    nevents = lst.FindObject('hSelEvents').GetBinContent(4)
    rawhist = lst.FindObject('hMassPtN3')
    rawmix = lst.FindObject('hMiMassPtN3')
    return [nevents, rawhist, rawmix]


def main():
    canvas = ROOT.TCanvas('c1', 'Canvas', 1000, 500)
    nfile = ROOT.TFile('input-data/LHC16k-NoBadmap.root')

    first = Spectrum(my_input('input-data/LHC16k.root'), label = 'BadMap', mode='q').evaluate()
    second = Spectrum(example_input('input-data/LHC16k-NoBadmap.root'), label = 'Tender', mode='q').evaluate()

    import spectrum.comparator as cmpr
    diff = cmpr.Comparator()
    diff.compare_lists_of_histograms(first, second)


if __name__ == '__main__':
    main()