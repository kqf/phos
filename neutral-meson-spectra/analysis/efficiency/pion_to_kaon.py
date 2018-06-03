import unittest
from spectrum.broot import BROOT as br
from spectrum.input import SingleHistInput
from spectrum.transformer import TransformerBase
from spectrum.pipeline import ReducePipeline, ParallelPipeline
from spectrum.comparator import Comparator
from spectrum.output import AnalysisOutput
from vault.datavault import DataVault


class HistSum(TransformerBase):
    def __init__(self, names):
        super(HistSum, self).__init__()
        self.pipeline = ReducePipeline(
            ParallelPipeline([
                (name, SingleHistInput(name)) for name in names
            ]),
            br.sum
        )


class KaonToPionRatio(TransformerBase):
    def __init__(self, pions, kaons):
        super(KaonToPionRatio, self).__init__()
        self.pipeline = ReducePipeline(
            ParallelPipeline([
                ('kaons', HistSum(kaons)),
                ('pions', HistSum(pions))
            ]),
            Comparator().compare
        )


class TestPionToKaonRatio(unittest.TestCase):
    def test_ratio(self):
        estimator = KaonToPionRatio(
            kaons=["hPt_K^{+}_", "hPt_K^{-}_"],
            pions=["hPt_#pi^{+}_", "hPt_#pi^{-}_"],
        )

        loggs = AnalysisOutput("calculate_pion_to_kaon", particle="")
        output = estimator.transform(
            [[DataVault().input("pythia8", "kaon2pion")] * 2] * 2,
            loggs
        )
