from spectrum.analysis import Analysis
from spectrum.comparator import Comparator
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


MC_HIGH = DataVault().input("single #pi^{0}", "high", listname="PhysEff")


def test_background_fitting():
    loggs = AnalysisOutput("fixed cb parameters", "#pi^{0}")
    options = Options.spmc((4.0, 20.0))

    outputs1 = Analysis(options).transform(MC_HIGH, loggs)

    loggs = AnalysisOutput("relaxed cb parameters", "#pi^{0}")
    options = Options.spmc((4.0, 20.0))
    options.signalp.relaxed = True

    outputs2 = Analysis(options).transform(MC_HIGH, loggs)

    diff = Comparator()
    for parameter in zip(outputs1, outputs2):
        diff.compare(*parameter)
