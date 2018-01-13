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



# This test is needed to check if the dataset does contain 
# correct spectrum, invariant mass distribution is ok, etc.

class TestDataSetForConsistency(unittest.TestCase):

    def setUp(self):
        fname = 'corrected/LHC16i-muon-calo-pass1.root' 
        inputs = Input(fname, 'PhysTender', 'MassPt', label='old')
        options = Options()
        self.sp_estimator = Spectrum(inputs, options)


    def test_dataset(self):
        observables = self.sp_estimator.evaluate()

        br.scalew(observables.spectrum)
        br.scalew(observables.npi0)

        c1 = gcanvas(1./2, resize=True)
        diff = cmpr.Comparator()
        for obs in observables:
            diff.compare(obs)



