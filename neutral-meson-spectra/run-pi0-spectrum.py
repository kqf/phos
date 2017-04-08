#!/usr/bin/python

import ROOT

from spectrum.spectrum import Spectrum
from spectrum.input import Input
from spectrum.sutils import get_canvas
from spectrum.options import Options

def main():
    g = lambda x, y, z: Spectrum(x, label=y, mode=z).evaluate()

    infile1 = 'input-data/LHC16.root'
    infile2 = 'input-data/LHC16-new.root'
    results = [
               g(Input(infile1, 'PhysTender').read(), 'old', 'q'), 
               g(Input(infile1, 'PhysOnlyTender').read(), 'new', 'q')
              ]
              
    c1 = get_canvas(1./2, resize=True)
    import spectrum.comparator as cmpr
    diff = cmpr.Comparator()
    diff.compare_set_of_histograms(results)

if __name__ == '__main__':
    main()