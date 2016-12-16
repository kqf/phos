#!/usr/bin/python

import ROOT

from spectrum.spectrum import PtAnalyzer, Spectrum
from spectrum.input import Input, TimecutInput

def main():
    canvas = ROOT.TCanvas('c1', 'Canvas', 1000, 500)

    # f = lambda x, y, z: Spectrum(x, label=y, mode=z).evaluate()
    f = lambda x, y, z: PtAnalyzer(x, label=y, mode=z).quantities()

    results = [
               f(Input('input-data/LHC16k-pass1-tender.root', 'PhysTender').read(), 'no timecut', 'q'),
               f(TimecutInput('input-data/LHC16k-pass1-ok.root', 'TimeTender', 'MassPtMainMain').read(), '23ns', 'q'), 
              ]

    import spectrum.comparator as cmpr
    diff = cmpr.Comparator()
    diff.compare_set_of_histograms(results)


if __name__ == '__main__':
    main()