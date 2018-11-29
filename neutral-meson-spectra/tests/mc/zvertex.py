#!/usr/bin/python

import unittest


from spectrum.input import read_histogram
from spectrum.comparator import Comparator


class CompareZVertexDistributions(unittest.TestCase):

    def setUp(self):
        self.productions = {'pythia': 'Pythia-LHC16-a5',
                            'jet jet': 'scaled-LHC17f8a',
                            'epos': 'EPOS-LHC16.root'}
        self.zveretx_data = self.zvertex('input-data/LHC16.root', 'data')

    def zvertex(self, filename, label='data'):
        hist = read_histogram(filename, 'QualOnlyTender',
                              'hZvertex', label=label)
        hist.Scale(1. / hist.Integral('w'))
        return hist

    def testProductions(self):
        mc_distributions = [self.zvertex(f, l)
                            for l, f in self.productions.iteritems()]

        oname = 'z-vertex-compared-{0}-data.pdf'
        for mc in mc_distributions:
            diff = Comparator(oname=oname.format(mc.label))
            diff.compare(mc, self.zveretx_data)
