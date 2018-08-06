import unittest
import ROOT
from spectrum.broot import BROOT as br
from spectrum.input import SingleHistInput
from spectrum.transformer import TransformerBase
from spectrum.pipeline import ReducePipeline, ParallelPipeline
from spectrum.pipeline import ComparePipeline
from spectrum.output import AnalysisOutput
from vault.datavault import DataVault
from spectrum.comparator import Comparator


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
    def __init__(self, pions, kaons, plot=False):
        super(KaonToPionRatio, self).__init__()
        self.pipeline = ComparePipeline([
            ("kaons", HistSum(kaons)),
            ("pions", HistSum(pions))
        ], plot)


class TestKaonToPionRatio(unittest.TestCase):

    # @unittest.skip("")
    def test_ratio(self):
        estimator = KaonToPionRatio(
            kaons=["hPt_K^{+}_", "hPt_K^{-}_"],
            pions=["hPt_#pi^{+}_", "hPt_#pi^{-}_"],
            plot=False,
        )

        loggs = AnalysisOutput("calculate_pion_to_kaon", particle="")

        infile = DataVault().input(
            "pythia8",
            "staging",
            listname="KaonToPionRatio"
        )

        mc = estimator.transform(
            [[infile] * 2] * 2,
            loggs
        )
        title = "Charged kaon to charged pion yields ratio"
        title += "; p_{T} , GeV/c"
        title += "; #frac{K^{+} + K^{-}}{#pi^{+} + #pi^{-}}"
        mc.SetTitle(title)
        mc.label = "PYTHIA8, #sqrt{s} = 13 TeV"

        estimator = ComparePipeline([
            ("kaon", SingleHistInput("hstat_kaon_pp13_sum")),
            ("pion", SingleHistInput("hstat_pion_pp13_sum")),
        ], plot=False)

        data = estimator.transform(
            [DataVault().input("kaon2pion")] * 2,
            AnalysisOutput("test")
        )
        data.SetTitle(title)
        data.label = "ALCIE, #sqrt{s} = 13 TeV, preliminary"
        Comparator().compare(mc)
        mc.SetAxisRange(1, 20, "X")
        mc, data = br.rebin_as(mc, data)
        data.SetAxisRange(1, 20, "X")
        data_mc_ratio = Comparator().compare(data, mc)

        fitfunc = ROOT.TF1(
            "feeddown_ratio",
            "TMath::Exp([0] * x  + [1]) * [2] + [3]", 1, 20)
        fitfunc.SetParameter(3, 6.0)
        data_mc_ratio.Fit(fitfunc, "R")
        data_mc_ratio.SetAxisRange(1, 20, "X")
        data_mc_ratio.SetName("testtest")
        Comparator().compare(data_mc_ratio)
