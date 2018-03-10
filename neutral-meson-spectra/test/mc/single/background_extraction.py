import unittest

import spectrum.sutils as su

from spectrum.processing import DataSlicer, RangeEstimator, DataExtractor, MassFitter
from spectrum.output import AnalysisOutput
from spectrum.input import Input
from spectrum.options import Options
from spectrum.pipeline import Pipeline
from spectrum.comparator import Comparator
from vault.datavault import DataVault
from spectrum.ptplotter import MassesPlot
from spectrum.ptplotter import MultiplePlotter


class MassExtractor(object):

    def __init__(self, options=Options()):
        super(MassExtractor, self).__init__()
        self.options = options
        self._loggs = None

    def transform(self, inputs, loggs):
        pipeline = Pipeline([
            ("input", inputs),
            ("slice", DataSlicer(self.options.pt)),
            ("fitmasses", MassFitter(self.options.invmass)),
        ])

        output = pipeline.transform(None, loggs)
        return output

class TestBackgroundSubtraction(unittest.TestCase):

    def test_background_fitting(self):
        loggs = AnalysisOutput("test_spmc_background", "#pi^{0}")

        estimator = MassExtractor(Options.spmc((7, 20)))
        masses = estimator.transform(
            Input(DataVault().file("single #pi^{0}", "high"), "PhysEff"),
            loggs
        )

        plotter = MultiplePlotter("test-multiple-plots")
        plotter.transform(masses, show=True)

        # for i, ptbin in enumerate(masses[14:]):
        #     canvas = su.canvas("test")
        #     MassesPlot().transform(ptbin, canvas)
        #     su.wait()



