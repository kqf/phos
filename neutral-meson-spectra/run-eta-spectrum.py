#!/usr/bin/python

import ROOT

from spectrum.spectrum import PtAnalyzer, Spectrum
from spectrum.input import Input, ExampleInput
from spectrum.sutils import get_canvas
from spectrum.options import Options

def main():
    c1 = get_canvas()
    # f = lambda x, y, z: Spectrum(x, label=y, mode=z).evaluate()
    f = lambda x, y, z: PtAnalyzer(x, label=y, mode=z, options=Options(particle='eta')).quantities()

    infile = 'input-data/LHC16-new.root'
    results = [
               f(Input(infile, 'EtaTender').read(), 'strict', 'v'), 
               f(Input(infile, 'EtaOnlyTender').read(), 'standard', 'v')
              ]

    import spectrum.comparator as cmpr
    diff = cmpr.Comparator()
    diff.compare_set_of_histograms(results)

if __name__ == '__main__':
    main()