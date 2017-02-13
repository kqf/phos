#!/usr/bin/python

import ROOT

from spectrum.spectrum import PtAnalyzer, Spectrum
from spectrum.input import Input, ExampleInput
from spectrum.sutils import get_canvas

def main():
    c1 = get_canvas()
    g = lambda x, y, z: Spectrum(x, label=y, mode=z).evaluate()
    f = lambda x, y, z: PtAnalyzer(x, label=y, mode=z).quantities()

    infile = 'input-data/LHC16.root'
    results = [
               g(Input(infile, 'PhysTender').read(), '5#sigma', 'q'), 
               g(Input(infile, 'PhysTender').read(), 'strict', 'q')
              ]

    import spectrum.comparator as cmpr
    diff = cmpr.Comparator()
    diff.compare_set_of_histograms(results)

if __name__ == '__main__':
    main()