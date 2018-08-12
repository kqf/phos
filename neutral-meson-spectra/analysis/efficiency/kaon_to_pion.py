import unittest
from collections import namedtuple

import ROOT
from spectrum.broot import BROOT as br
from spectrum.input import SingleHistInput
from spectrum.transformer import TransformerBase
from spectrum.pipeline import ReducePipeline, ParallelPipeline
from spectrum.pipeline import ReducePipelineLoggs
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


K2POptions = namedtuple("K2POptions", ["pions", "kaons"])
DoubleK2POptions = namedtuple("DoubleK2POptions", ["data", "mc"])


class KaonToPionRatioMC(TransformerBase):
    def __init__(self, options, plot=False):
        super(KaonToPionRatioMC, self).__init__()
        self.pipeline = ComparePipeline([
            ("kaons", HistSum(options.kaons)),
            ("pions", HistSum(options.pions))
        ], plot)


# NB: Real Data distributions are stored in
#     separate files produced by ALCIE
class KaonToPionRatioData(TransformerBase):
    def __init__(self, options, plot=False):
        super(KaonToPionRatioData, self).__init__()
        self.pipeline = ComparePipeline([
            ("kaons", SingleHistInput(options.kaons)),
            ("pions", SingleHistInput(options.pions)),
        ], plot)


def rebin_compare(inputs, loggs):
    data, mc = inputs
    title = "Charged kaon to charged pion yields ratio"
    title += "; p_{T} , GeV/c"
    title += "; #frac{K^{+} + K^{-}}{#pi^{+} + #pi^{-}}"
    mc.SetTitle(title)
    mc.label = "PYTHIA8, #sqrt{s} = 13 TeV"
    data.SetTitle(title)
    data.label = "ALCIE, #sqrt{s} = 13 TeV, preliminary"
    mc.SetAxisRange(0.2, 20, "X")
    mc, data = br.rebin_as(mc, data)
    data.SetAxisRange(0.2, 20, "X")
    return Comparator(loggs=loggs).compare(data, mc)


class KaonToPionDoubleRatio(TransformerBase):
    def __init__(self, options, plot=False):
        super(KaonToPionDoubleRatio, self).__init__()
        self.pipeline = ReducePipelineLoggs(
            ParallelPipeline([
                ("data", KaonToPionRatioData(options.data)),
                ("mc", KaonToPionRatioMC(options.mc)),
            ]),
            rebin_compare
        )


class TestDoubleKaonToPionRatio(unittest.TestCase):

    # @unittest.skip("")
    def test_ratio(self):
        options = DoubleK2POptions(
            data=K2POptions(
                kaons="hstat_kaon_pp13_sum",
                pions="hstat_pion_pp13_sum"
            ),
            mc=K2POptions(
                kaons=["hPt_K^{+}_", "hPt_K^{-}_"],
                pions=["hPt_#pi^{+}_", "hPt_#pi^{-}_"]
            )
        )

        estimator = KaonToPionDoubleRatio(options, plot=True)
        pythia8 = DataVault().input("pythia8", listname="KaonToPionRatio")
        loggs = AnalysisOutput("calculate_pion_to_kaon", particle="")
        output = estimator.transform(
            [
                [DataVault().input("kaon2pion")] * 2,
                [[pythia8] * 2] * 2
            ],
            loggs
        )
        loggs.plot()
        return

        fitfunc = ROOT.TF1(
            "feeddown_ratio",
            "TMath::Exp([0] * x  + [1]) * [2] + [3]", 1, 20)
        fitfunc.SetParameter(3, 6.0)
        data_mc_ratio.Fit(fitfunc, "R")
        data_mc_ratio.SetAxisRange(1, 20, "X")
        data_mc_ratio.SetName("testtest")
        Comparator().compare(data_mc_ratio)
