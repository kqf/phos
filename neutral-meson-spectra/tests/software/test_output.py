import pytest

import ROOT
from spectrum.output import open_loggs
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


@pytest.fixture
def data():
    return (None, None)


def test_the_output(data):
    estimator = Pipeline([
        ('dummy1', DummyTransformer("histname1")),
        ('dummy2', DummyTransformer("histname2")),
    ])
    with open_loggs("test loggs") as loggs:
        estimator.transform(data, loggs)
