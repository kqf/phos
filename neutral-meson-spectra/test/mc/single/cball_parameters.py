import unittest

from spectrum.analysis import Analysis
from spectrum.comparator import Comparator
from spectrum.input import Input
from spectrum.options import Options
from spectrum.output import AnalysisOutput
from spectrum.pipeline import Pipeline
from spectrum.processing import DataSlicer, MassFitter
from vault.datavault import DataVault


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
        inputs = Input(
            DataVault().file(
                "single #pi^{0} iteration d3 nonlin13",
                "high"
            ),
            "PhysEff"
        )

        loggs = AnalysisOutput("fixed cb parameters", "#pi^{0}")
        options = Options.spmc((7, 20))

        outputs1 = Analysis(options).transform(inputs, loggs)

        loggs = AnalysisOutput("relaxed cb parameters", "#pi^{0}")
        options = Options.spmc((7, 20))
        options.signalp.relaxed = True

        outputs2 = Analysis(options).transform(inputs, loggs)

        diff = Comparator()
        for parameter in zip(outputs1, outputs2):
            diff.compare(*parameter)
