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


# float inBack(float x)
# {
#     if(x < [0]) return[0]
#     if(x > [1]) return[1]
#     return x * x * (([2] + [1]) * x - [2])
# }


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
        double_ratio = estimator.transform(
            [
                [DataVault().input("kaon2pion")] * 2,
                [[pythia8] * 2] * 2
            ],
            loggs
        )
        double_ratio.SetMarkerSize(0)
        fitfunc = ROOT.TF1(
            "feeddown_ratio",
            "[3] * x *(([4] + [5]) * x - [5]) + "
            "[0] * (1 + [1] * TMath::Exp(-x * x/ [2]))", 0, 20)
        fitfunc.SetParameter(0, 1.53561e+00)
        fitfunc.SetParameter(1, -4.69350e-01)
        fitfunc.SetParameter(2, 2.38042e-01)
        fitfunc.SetParameter(3, -8.01155e-02)
        fitfunc.SetParameter(4, 6.30860e-01)
        fitfunc.SetParameter(5, -7.21683e-01)

        double_ratio.Fit(fitfunc, "R")
        fitfunc.SetRange(0, 20)
        print(br.pars(fitfunc))

        title = "Chi2/ndf = " + str(fitfunc.GetChisquare() / fitfunc.GetNDF())
        double_ratio.SetTitle(title)
        double_ratio.label = "pp at \sqrt{s} = 13 TeV"
        double_ratio.SetName("kaon2pion")
        Comparator().compare(double_ratio)
