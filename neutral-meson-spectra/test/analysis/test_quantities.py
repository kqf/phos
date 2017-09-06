#!/usr/bin/python

import unittest
import operator as op

import ROOT
from spectrum.spectrum import Spectrum
from spectrum.input import Input
from spectrum.sutils import get_canvas
from spectrum.options import Options
import spectrum.comparator as cmpr

from spectrum.broot import BROOT as br


class TestRawQauntities(unittest.TestCase):

    def setUp(self):
        self.inputs = Input('LHC16-old.root', 'PhysTender', 'MassPtN3'), Input('LHC16.root', 'PhysTender', 'MassPt')
        self.options_pi0 = Options('old', 'q'),  Options('new', 'q')
        self.options_eta = Options('old', 'q', particle = 'eta'),  Options('new', 'q', particle = 'eta')


    def run_analysis(self, inputs, options):
        spectrums = map(Spectrum, inputs, options)
        observables = map(op.methodcaller('evaluate'), spectrums)

        for obs in observables:
            br.scalew(obs.spectrum)
            br.scalew(obs.npi0)

        c1 = get_canvas(1./2, resize=True)
        diff = cmpr.Comparator()
        diff.compare(observables)


    def test_pi0(self):
        self.run_analysis(self.inputs, self.options_pi0)


    def test_eta(self):
        self.run_analysis(self.inputs, self.options_eta)


