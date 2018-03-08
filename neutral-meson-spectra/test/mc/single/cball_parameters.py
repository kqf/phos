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
from spectrum.analysis import Analysis


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
        loggs = AnalysisOutput("fixed cb parameters", "#pi^{0}")
        options = Options.spmc((7, 20))


        estimator = Analysis(options)
        outputs1 = estimator.transform(
            Input(DataVault().file("single #pi^{0}", "high"), "PhysEff"),
            loggs
        )

        loggs = AnalysisOutput("relaxed cb parameters", "#pi^{0}")
        options = Options.spmc((7, 20))
        options.backgroundp.relaxed = True


        estimator = Analysis(options)
        outputs2 = estimator.transform(
            Input(DataVault().file("single #pi^{0}", "high"), "PhysEff"),
            loggs
        )

        diff = Comparator()
        for parameter in zip(outputs1, outputs2):
            diff.compare(*parameter)







