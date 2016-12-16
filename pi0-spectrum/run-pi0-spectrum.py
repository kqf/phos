#!/usr/bin/python

import ROOT

from spectrum.spectrum import PtAnalyzer, Spectrum
from spectrum.input import Input, ExampleInput

def main():
    canvas = ROOT.TCanvas('c1', 'Canvas', 1000, 500)

    # f = lambda x, y, z: Spectrum(x, label=y, mode=z).evaluate()
    f = lambda x, y, z: PtAnalyzer(x, label=y, mode=z).quantities()

    infile = 'input-data/LHC16k-MyTask.root'
    results = [
               f(Input(infile, 'PhysNoTender').read(), 'my task no tender', 'q'),
               f(Input(infile, 'PhysTender').read(), 'my task and tender', 'q'), 
               f(Input(infile, 'PhysOnlyTender').read(), 'my task only tender', 'q'), 
               f(ExampleInput('input-data/LHC16k-NoBadmap.root').read(), 'Tender No BMap', 'q')
              ]

    import spectrum.comparator as cmpr
    diff = cmpr.Comparator()
    diff.compare_set_of_histograms(results)

if __name__ == '__main__':
    main()