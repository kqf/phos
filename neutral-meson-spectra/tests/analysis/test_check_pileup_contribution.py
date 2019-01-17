import pytest

from lazy_object_proxy import Proxy
from spectrum.analysis import Analysis
from spectrum.options import Options
from spectrum.pipeline import TransformerBase
from spectrum.pipeline import Pipeline, HistogramSelector
from spectrum.pipeline import ComparePipeline
from vault.datavault import DataVault
from spectrum.output import AnalysisOutput


DATASET = Proxy(
    lambda:
    (
        DataVault().input("data", "latest", "Time",
                          histname="MassPtMainMain"),  # cut
        DataVault().input("data", "latest", "Time"),  # no cut
    )

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
def test_pileup():
    estimator = PileupEstimator(plot=True)
    estimator.transform(DATASET, loggs=AnalysisOutput("pileup contribution"))
