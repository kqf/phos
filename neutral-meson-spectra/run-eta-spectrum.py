#!/usr/bin/python

import ROOT

from spectrum.spectrum import PtAnalyzer, Spectrum
from spectrum.input import Input, ExampleInput
from spectrum.sutils import get_canvas

def main():
    c1 = get_canvas()
    # f = lambda x, y, z: Spectrum(x, label=y, mode=z).evaluate()
    f = lambda x, y, z: PtAnalyzer(x, label=y, mode=z, particle='eta').quantities()

    infile = 'input-data/LHC16-new.root'
    results = [
               f(Input(infile, 'EtaTimeTender').read(), 'strict', 'q'), 
               f(Input(infile, 'EtaTimeOnlyTender').read(), 'standard', 'q')
              ]

    import spectrum.comparator as cmpr
    diff = cmpr.Comparator()
    diff.compare_set_of_histograms(results)

if __name__ == '__main__':
    main()