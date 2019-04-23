import pytest
import ROOT

from phasegen.analysis import Analysis, AnalysisBuilder
from phasegen.analysis import root_file


class SimpleAnalysis(object):
    def __init__(self, ofile="output.root"):
        super(SimpleAnalysis, self).__init__()
        self.hist = ROOT.TH1F("hMomentum", "test", 10, 0, 3)
        self.ofile = ofile

    def transform(self, particles):
        _, original = particles
        self.hist.Fill(original.P())

    def write(self):
        with root_file(self.ofile):
            self.hist.Write()


@pytest.mark.parametrize("generator_type", [
    "normal",
    "randomized"
])
def test_analysis(generator_type, config):
    builder = AnalysisBuilder(config)
    builder.generator_type = generator_type

    selections = Analysis(builder).transform([
        SimpleAnalysis()
    ])

    for selection in selections:
        selection.write()
