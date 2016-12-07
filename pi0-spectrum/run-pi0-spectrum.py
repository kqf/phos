#!/usr/bin/python

import ROOT

from spectrum.spectrum import PtAnalyzer, Spectrum

def my_input(filename, f = lambda x: x.PhysNoTender):
    lst = f(ROOT.TFile(filename))
    nevents = lst.FindObject('EventCounter').GetBinContent(2)
    rawhist = lst.FindObject('hMassPtN3')
    rawmix = lst.FindObject('hMixMassPtN3')
    return [nevents, rawhist, rawmix]

def example_input(filename):
    lst = ROOT.TFile(filename).Data
    nevents = lst.FindObject('hSelEvents').GetBinContent(4)
    # pattern = "MassPtN3"
    pattern = "MassPtA10vtx10"
    rawhist = lst.FindObject('h' + pattern)
    rawmix = lst.FindObject('hMi' + pattern)
    return [nevents, rawhist, rawmix]


def main():
    canvas = ROOT.TCanvas('c1', 'Canvas', 1000, 500)

    # f = lambda x, y, z: Spectrum(x, label=y, mode=z).evaluate()
    f = lambda x, y, z: PtAnalyzer(x, label=y, mode=z).quantities()

    # first = f(example_input('input-data/LHC16k-pass1-tender-and-my-bmap.root'), 'BadMap', 'v')
    results = [
               f(my_input('input-data/LHC16k-MyTask.root'), 'my task no tender', 'q'),
               f(my_input('input-data/LHC16k-MyTask.root', lambda x: x.PhysTender), 'my task and tender', 'q'), 
               f(my_input('input-data/LHC16k-MyTask.root', lambda x: x.PhysOnlyTender), 'my task only tender', 'q'), 
               f(example_input('input-data/LHC16k-NoBadmap.root'), 'Tender No BMap', 'q')
              ]

    import spectrum.comparator as cmpr
    diff = cmpr.Comparator()
    # diff.compare_lists_of_histograms([first, second])
    diff.compare_set_of_histograms(results)


if __name__ == '__main__':
    main()