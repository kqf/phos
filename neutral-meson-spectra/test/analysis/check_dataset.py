#!/usr/bin/python

import sys
import unittest
import operator as op

import ROOT
from spectrum.analysis import Analysis
from spectrum.input import Input
from spectrum.sutils import gcanvas
from spectrum.options import Options
from spectrum.output import AnalysisOutput
import spectrum.comparator as cmpr

from spectrum.broot import BROOT as br
from vault.datavault import DataVault



# This test is needed to check if the dataset does contain
# correct spectrum, invariant mass distribution is ok, etc.

class TestDataSetForConsistency(unittest.TestCase):

    def test_dataset(self):
        # Configure the analysis
        options = Options()
        options.output.scalew_spectrum = True
        estimator = Analysis(options)

        # Analyze the data
        observables = estimator.transform(
           DataVault().input('data', 'LHC17 qa1', 'Phys', label='old'),
           AnalysisOutput("consistency check", "\pi^{0}")
        )

        c1 = gcanvas(1./2, resize=True)
        diff = cmpr.Comparator()
        for obs in observables:
            diff.compare(obs)



