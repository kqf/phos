#!/usr/bin/python

import ROOT

from spectrum.spectrum import PtAnalyzer, Spectrum
from spectrum.input import Input, ExampleInput
from spectrum.sutils import get_canvas
from spectrum.options import Options

def main():
    # c1 = get_canvas(1./ 2)
    f = lambda x, y, z: Spectrum(x, label=y, mode=z, options=Options(particle='eta')).evaluate()

    infile = 'input-data/LHC16-new.root'
    results = [
               f(Input(infile, 'EtaTender').read(), 'A < 0.7', 'q'), 
               f(Input(infile, 'PhysTender').read(), 'A < 1.0', 'q')
              ]

    import spectrum.comparator as cmpr
    diff = cmpr.Comparator(size=(1./2, 1))
    diff.compare_set_of_histograms(results)

if __name__ == '__main__':
    main()