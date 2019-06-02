import pytest
from collections import namedtuple

import ROOT
from spectrum.broot import BROOT as br
from spectrum.input import SingleHistInput
from spectrum.pipeline import TransformerBase
from spectrum.pipeline import ReducePipeline, ParallelPipeline
from spectrum.pipeline import ComparePipeline
from spectrum.pipeline import Pipeline
from spectrum.output import open_loggs
from vault.datavault import DataVault
from spectrum.comparator import Comparator


class HistSum(TransformerBase):
    def __init__(self, names):
        super(HistSum, self).__init__()
        self.pipeline = ReducePipeline(
            ParallelPipeline([
                (name, SingleHistInput(name)) for name in names
            ]),
            lambda x, loggs: br.sum(x)
        )


K2POptions = namedtuple("K2POptions", ["pions", "kaons"])
DoubleK2POptions = namedtuple("DoubleK2POptions", ["data", "mc", "fitfunc"])


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
    return Comparator().compare(data, mc, loggs=loggs)


class DoubleRatioFitter(TransformerBase):
    def __init__(self, fitfunc, plot=False):
        super(DoubleRatioFitter, self).__init__(plot)
        self.fitfunc = fitfunc

    def transform(self, double_ratio, loggs):
        double_ratio.SetMarkerSize(0)
        double_ratio.Fit(self.fitfunc, "R")
        self.fitfunc.SetRange(0, 20)
        title = "Chi2/ndf = " + \
            str(self.fitfunc.GetChisquare() / self.fitfunc.GetNDF())
        double_ratio.SetTitle(title)
        double_ratio.label = "pp at \sqrt{s} = 13 TeV"
        double_ratio.SetName("kaon2pion")
        print(br.pars(self.fitfunc))
        return double_ratio


class KaonToPionDoubleRatio(TransformerBase):
    def __init__(self, options, plot=False):
        super(KaonToPionDoubleRatio, self).__init__()
        double_ratio = ReducePipeline(
            ParallelPipeline([
                ("data", KaonToPionRatioData(options.data)),
                ("mc", KaonToPionRatioMC(options.mc)),
            ]),
            rebin_compare
        )

        self.pipeline = Pipeline([
            ("data_mc_ratio", double_ratio),
            ("fit", DoubleRatioFitter(options.fitfunc, plot)),
        ])


@pytest.fixture
def real_data():
    return (
        DataVault().input("kaon2pion"),
        DataVault().input("kaon2pion"),
    )


@pytest.fixture
def mc_data():
    return (
        (
            DataVault().input("pythia8", listname="KaonToPionRatio"),
            DataVault().input("pythia8", listname="KaonToPionRatio"),
        ),
        (
            DataVault().input("pythia8", listname="KaonToPionRatio"),
            DataVault().input("pythia8", listname="KaonToPionRatio"),
        ),
    )


@pytest.fixture
def data(real_data, mc_data):
    return (real_data, mc_data)


@pytest.mark.skip("")
def test_draw_ratio_mc(mc_data):
    options = K2POptions(
        kaons=["hPt_K^{+}_", "hPt_K^{-}_"],
        pions=["hPt_#pi^{+}_", "hPt_#pi^{-}_"]
    )
    return KaonToPionRatioMC(options).transform(mc_data, {})


@pytest.mark.thesis
def test_ratio(data):
    fitfunc = ROOT.TF1(
        "feeddown_ratio",
        "[3] * x *(([4] + [5]) * x - [5]) + "
        "[0] * (1 + [1] * TMath::Exp(-x * x/ [2]))", 0, 20)
    fitfunc.SetParameter(0, 1.53561e-02)
    fitfunc.SetParameter(1, -4.69350e-01)
    fitfunc.SetParameter(2, 2.38042e-01)
    fitfunc.SetParameter(3, -8.01155e-04)
    fitfunc.SetParameter(4, 6.30860e-01)
    fitfunc.SetParameter(5, -7.21683e-01)

    options = DoubleK2POptions(
        data=K2POptions(
            kaons="hstat_kaon_pp13_sum",
            pions="hstat_pion_pp13_sum"
        ),
        mc=K2POptions(
            kaons=["hPt_K^{+}_", "hPt_K^{-}_"],
            pions=["hPt_#pi^{+}_", "hPt_#pi^{-}_"]
        ),
        fitfunc=fitfunc
    )

    estimator = KaonToPionDoubleRatio(options, plot=True)
    with open_loggs("pion to kaon") as loggs:
        double_ratio = estimator.transform(data, loggs)
        Comparator().compare(double_ratio)
