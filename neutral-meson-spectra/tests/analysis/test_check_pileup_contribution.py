import pytest

from spectrum.analysis import Analysis
from spectrum.options import Options
from spectrum.pipeline import TransformerBase
from spectrum.pipeline import Pipeline, HistogramSelector
from spectrum.pipeline import ComparePipeline
from vault.datavault import DataVault
from spectrum.output import open_loggs


@pytest.fixture
def data():
    return (
        DataVault().input("data", "latest", "Time",
                          histname="MassPtMainMain"),  # cut
        DataVault().input("data", "latest", "Time"),  # no cut
    )


class PileupEstimator(TransformerBase):
    def __init__(self, options=Options(), plot=False):
        super(PileupEstimator, self).__init__(plot)
        self.pipeline = ComparePipeline([
            ('12.5 ns', Pipeline([
                ('analysis', Analysis(options, plot)),
                ('spectrum', HistogramSelector("nmesons"))
            ])),
            ('no cut', Pipeline([
                ('analysis', Analysis(options, plot)),
                ('spectrum', HistogramSelector("nmesons"))
            ])),
        ], plot)


@pytest.mark.onlylocal
def test_pileup(data):
    estimator = PileupEstimator(plot=True)
    with open_loggs("pileup contribution") as loggs:
        estimator.transform(data, loggs)
