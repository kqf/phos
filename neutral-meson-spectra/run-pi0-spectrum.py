#!/usr/bin/python

import ROOT

from spectrum.spectrum import Spectrum
from spectrum.input import Input
from spectrum.sutils import get_canvas, scalew
from spectrum.options import Options

def main():
    g = lambda x, y: Spectrum(x, y).evaluate()

    inputs = Input('LHC16-old.root', 'PhysTender', 'MassPtN3'), Input('LHC16.root', 'PhysTender', 'MassPt')
    options = Options('old', 'q'),  Options('new', 'q')
    results = map(g, inputs, options)
              
    for r in results: 
      scalew(r.spectrum)
              
    c1 = get_canvas(1./2, resize=True)
    import spectrum.comparator as cmpr
    diff = cmpr.Comparator()
    diff.compare_set_of_histograms(results)

if __name__ == '__main__':
    main()