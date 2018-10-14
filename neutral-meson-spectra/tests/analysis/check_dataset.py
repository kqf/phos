#!/usr/bin/python

import unittest

import spectrum.comparator as cmpr
from spectrum.analysis import Analysis
from spectrum.options import Options
from spectrum.output import AnalysisOutput
from vault.datavault import DataVault


# This test is needed to check if the dataset does contain
# correct spectrum, invariant mass distribution is ok, etc.

class TestDataSetForConsistency(unittest.TestCase):

    def test_dataset(self):
        # Configure the analysis
        options = Options(particle="#eta")
        options.output.scalew_spectrum = True
        estimator = Analysis(options)

        # Analyze the data
        observables = estimator.transform(
            DataVault().input('data'),
            AnalysisOutput("ALICE, \sqrt{s} = 13 TeV", "\pi^{0}")
        )

        # c1 = gcanvas(1. / 2, resize=True)
        diff = cmpr.Comparator()
        for obs in observables:
            diff.compare(obs)
