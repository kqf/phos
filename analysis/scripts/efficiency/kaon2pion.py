import pytest

import ROOT
import spectrum.broot as br
from spectrum.pipeline import RebinTransformer
from spectrum.tools.kaon2pion import KaonToPionDoubleRatio
from spectrum.tools.kaon2pion import DoubleK2POptions
from spectrum.output import open_loggs
from spectrum.vault import DataVault
from spectrum.plotter import plot


@pytest.fixture
def data():
    real_data = (
        DataVault().input("kaon2pion", histname="hstat_kaon_pp13_sum"),
        DataVault().input("kaon2pion", histname="hstat_pion_pp13_sum"),
    )

    mc_data = (
        (
            DataVault().input("pythia8", "kaon2pion", histname="hPt_K^{+}_"),
            DataVault().input("pythia8", "kaon2pion", histname="hPt_K^{-}_"),
        ),
        (
            DataVault().input("pythia8", "kaon2pion", histname="hPt_#pi^{+}_"),
            DataVault().input("pythia8", "kaon2pion", histname="hPt_#pi^{-}_"),
        ),
    )
    return real_data, mc_data


def reduce_func(inputs, loggs, stop):
    fitfunc = ROOT.TF1(
        "KpiRatio",
        "[3] * x * x + [4] * x * x - [4] * x + "
        "[0] * (1 + [1] * TMath::Exp(-x * x/ [2]))", 0.3, 20)
    fitfunc.SetTitle("Fit")
    fitfunc.SetLineColor(ROOT.kBlack)
    fitfunc.SetLineStyle(9)
    fitfunc.SetParNames(*["A", "B", "S", "C", "D"])
    fitfunc.SetParameter(0, 1.760221482495616)
    fitfunc.SetParameter(1, -0.4026614560039952)
    fitfunc.SetParameter(2, 0.5459275534441625)
    fitfunc.SetParameter(3, -0.15120526703793247)
    fitfunc.SetParameter(4, 0.1673495588004339)

    data, mc_ = inputs
    data.SetTitle(
        "Data; #it{p}_{T} (GeV/#it{c});"
        "(#frac{#it{K}^{ +} + #it{K}^{ -}}{#pi^{+} + #pi^{-}})^{data}"
    )
    mc_.SetTitle(
        "MC; #it{p}_{T} (GeV/#it{c});"
        "(#frac{#it{K}^{ +} + #it{K}^{ -}}{#pi^{+} + #pi^{-}})^{mc}"
    )
    mc = RebinTransformer(True, br.edges(data)).transform(mc_, loggs)
    plot(
        [data, mc],
        stop=stop,
        xlimits=(0.3, 20),
        ylimits=(0.0, 0.7),
        ytitle="#frac{#it{K}^{ +} + #it{K}^{ -}}{#pi^{+} + #pi^{-}}",
        logy=False,
        logx=False,
        legend_pos=(0.2, 0.7, 0.4, 0.85),
        oname="results/analysis/kaon2pion_ratio.pdf",
    )

    double_ratio = br.ratio(data, mc)
    double_ratio.Fit(fitfunc, "RQWW")
    plot(
        [double_ratio, fitfunc],
        stop=stop,
        xlimits=(0.3, 20),
        logy=False,
        logx=True,
        oname="results/analysis/kaon2pion_doubleratio.pdf",
    )
    br.report(fitfunc)
    return double_ratio


@pytest.mark.thesis
@pytest.mark.onlylocal
def test_ratio(data, stop):
    estimator = KaonToPionDoubleRatio(DoubleK2POptions(reduce_func), plot=stop)
    with open_loggs() as loggs:
        estimator.transform(data, loggs)
