#!/usr/bin/python

import ROOT

from spectrum.spectrum import PtAnalyzer, Spectrum
from spectrum.input import Input, ExampleInput
from spectrum.sutils import get_canvas

def main():
    g = lambda x, y, z, w: Spectrum(x, label=y, mode=z, relaxedcb=w).evaluate()
    f = lambda x, y, z: PtAnalyzer(x, label=y, mode=z).quantities()

    infile = 'input-data/LHC16.root'
    results = [
               g(Input(infile, 'PhysTender').read(), 'fixed', 'q', True), 
               g(Input(infile, 'PhysTender').read(), 'relaxed', 'q', False)
              ]

    c1 = get_canvas(1/2.)
    import spectrum.comparator as cmpr
    diff = cmpr.Comparator()
    diff.compare_set_of_histograms(results)

if __name__ == '__main__':
    main()