#!/usr/bin/python

import ROOT

from spectrum.spectrum import Spectrum
from spectrum.input import Input
from spectrum.sutils import get_canvas
from spectrum.options import Options

def main():
    g = lambda x, y, z, w: Spectrum(x, label=y, mode=z, options=w).evaluate()

    infile = 'input-data/LHC16.root'
    results = [
               g(Input(infile, 'PhysTender').read(), 'fixed cb parameters', 'q', Options(relaxedcb = False)), 
               g(Input(infile, 'PhysTender').read(), 'relaxed cb parameters', 'q', Options(relaxedcb = True))
              ]

    c1 = get_canvas(1/2.)
    import spectrum.comparator as cmpr
    diff = cmpr.Comparator()
    diff.compare_set_of_histograms(results)

if __name__ == '__main__':
    main()