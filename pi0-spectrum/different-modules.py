#!/usr/bin/python

import ROOT

from spectrum.spectrum import PtAnalyzer, Spectrum

def from_list(lst, name, nevents):
    rawhist = lst.FindObject('h' + name)
    rawmix = lst.FindObject('hMix' + name)
    if rawhist.GetXaxis().GetBinCenter(rawhist.FindFirstBinAbove()) > 0.135: return None
    return [nevents, rawhist, rawmix]

def module_hitograms(filename, name = 'MassPt'):

    lst = ROOT.TFile(filename).PhysTender
    nevents = lst.FindObject('EventCounter').GetBinContent(2)

    names = ['SM%dSM%d' % (i, j) for i in range(1, 5) for j in range(i, 5) ] 
    hists = map(lambda x: from_list(lst, name + x, nevents), names)

    input_data  = ((h, l) for h, l in zip(hists, names) if h)
    return zip(*input_data)



def main():
    canvas = ROOT.TCanvas('c1', 'Canvas', 1000, 500)

    # f = lambda x, y, z: Spectrum(x, label=y, mode=z).evaluate()
    f = lambda x, y: PtAnalyzer(x, label=y, mode='q').quantities()

    results = map(f, *module_hitograms('input-data/LHC16k-MyTask.root'))

    import spectrum.comparator as cmpr
    diff = cmpr.Comparator()
    # diff.compare_lists_of_histograms([first, second])
    diff.compare_set_of_histograms(results)


if __name__ == '__main__':
    main()