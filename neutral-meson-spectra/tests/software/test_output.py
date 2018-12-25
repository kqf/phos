import ROOT
from spectrum.output import AnalysisOutput
from spectrum.pipeline import Pipeline
from spectrum.pipeline import TransformerBase


class DummyTransformer(TransformerBase):

    def __init__(self, name, plot=False):
        super(DummyTransformer, self).__init__(plot)
        self.name = name

    def transform(self, output, loggs):
        hist = ROOT.TH1F(self.name, "output", 100, -3, 3)
        hist.FillRandom("gaus")
        loggs.update({"dummy_outputs": hist})
        return hist


DUMMY_DATASET = (
    None,
    None
)


def test_the_output():
    loggs = AnalysisOutput("test_loggs_output")
    estimator = Pipeline([
        ('dummy1', DummyTransformer("histname1")),
        ('dummy2', DummyTransformer("histname2")),
    ])
    estimator.transform(DUMMY_DATASET, loggs)
    loggs.plot()
