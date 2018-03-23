#!/usr/bin/python

from spectrum.spectrum import Spectrum
from spectrum.input import Input
from spectrum.options import Options
from spectrum.sutils import gcanvas, adjust_canvas
from spectrum.pipeline import ParallelPipeline, ReducePipeline
from vault.datavault import DataVault
from spectrum.analysis import Analysis
from spectrum.output import AnalysisOutput
from spectrum.comparator import Comparator

import test.check_default
import unittest
import operator


def analyze(inputs, particle="#pi^{0}"):
    options = Options(particle=particle)
    estimator = ReducePipeline(
        ParallelPipeline([
            ('module{0}'.format(i), Analysis(options)) for i, _ in enumerate(inputs)
        ]),
        Comparator().compare
    )

    loggs = AnalysisOutput("compare_different_modules", particle=particle)
    estimator.transform(inputs, loggs)
    # loggs.plot()


class TestCheckModules(unittest.TestCase):
    def test_different_modules_pi0(self):
        inputs = Input.read_per_module(
            DataVault().file("data", "LHC17 qa1"),
            "Phys",
            same_module=True
        )
        analyze(inputs, "#pi^{0}")

    def test_different_modules_eta(self):
        inputs = Input.read_per_module(
            DataVault().file("data", "LHC17 qa1"),
            "Phys",
            same_module=True
        )
        analyze(inputs, "#eta")




if __name__ == '__main__':
    main()