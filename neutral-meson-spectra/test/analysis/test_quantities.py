#!/usr/bin/python

import sys
import unittest
import operator as op

import ROOT
from spectrum.spectrum import Spectrum
from spectrum.input import Input
from spectrum.sutils import gcanvas
from spectrum.options import Options
import spectrum.comparator as cmpr

from spectrum.broot import BROOT as br


class TestRawQauntities(unittest.TestCase):

    def setUp(self):
        self.inputs = Input('LHC16-old.root', 'PhysTender', 'MassPtN3'), Input('LHC16.root', 'PhysTender', 'MassPt')
        self.options_pi0 = Options('old', 'q'),  Options('new', 'q')
        self.options_eta = Options('old', 'q', particle = 'eta'),  Options('new', 'q', particle = 'eta')
        self.stop = 'discover' not in sys.argv


    def run_analysis(self, inputs, options):
        spectrums = map(Spectrum, inputs, options)
        observables = map(op.methodcaller('evaluate'), spectrums)

        for obs in observables:
            br.scalew(obs.spectrum)
            br.scalew(obs.npi0)

        c1 = gcanvas(1./2, resize=True)
        diff = cmpr.Comparator(stop = self.stop)
        diff.compare(observables)


    def test_pi0(self):
        self.run_analysis(self.inputs, self.options_pi0)


    def test_eta(self):
        self.run_analysis(self.inputs, self.options_eta)


