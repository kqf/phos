import unittest
import pytest

from spectrum.analysis import Analysis
from spectrum.options import Options
from spectrum.transformer import TransformerBase
from spectrum.pipeline import Pipeline, HistogramSelector
from spectrum.pipeline import ComparePipeline
from vault.datavault import DataVault
from spectrum.output import AnalysisOutput


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


class CheckPileup(unittest.TestCase):

    @pytest.mark.onlylocal
    def test_pileup(self):
        with_cut = DataVault().input("data",
                                     "latest",
                                     "Time",
                                     histname="MassPtMainMain")

        no_cut = DataVault().input("data",
                                   "latest",
                                   "Time"
                                   )
        estimator = PileupEstimator(plot=True)
        estimator.transform(
            [with_cut, no_cut],
            loggs=AnalysisOutput("pileup contribution")
        )
