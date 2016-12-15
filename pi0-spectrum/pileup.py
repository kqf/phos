#!/usr/bin/python

import ROOT

from spectrum.spectrum import PtAnalyzer, Spectrum

def my_input(filename, name = 'MassPtN3', f = lambda x: x.PhysTender):
    nevents = ROOT.TFile(filename).PhysTender.FindObject('EventCounter').GetBinContent(2)
    lst = f(ROOT.TFile(filename))
    rawhist = lst.FindObject('h' + name)
    rawmix = lst.FindObject('hMix' + name)
    return [nevents, rawhist, rawmix]


def main():
    canvas = ROOT.TCanvas('c1', 'Canvas', 1000, 500)

    # f = lambda x, y, z: Spectrum(x, label=y, mode=z).evaluate()
    f = lambda x, y, z: PtAnalyzer(x, label=y, mode=z).quantities()

    results = [
               f(my_input('input-data/LHC16k-pass1-tender.root'), 'no timecut', 'q'),
               f(my_input('input-data/LHC16k-pass1-half-almost-clean.root', 'MassPtMainMain' , lambda x: x.TimeTender), '23ns', 'q'), 
              ]

    import spectrum.comparator as cmpr
    diff = cmpr.Comparator()
    # diff.compare_lists_of_histograms([first, second])
    diff.compare_set_of_histograms(results)


if __name__ == '__main__':
    main()