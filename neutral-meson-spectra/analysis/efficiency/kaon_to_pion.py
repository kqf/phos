import pytest

import ROOT
import spectrum.broot as br
from spectrum.pipeline import RebinTransformer
from spectrum.tools.kaon2pion import KaonToPionDoubleRatio
from spectrum.tools.kaon2pion import DoubleK2POptions, K2POptions
from spectrum.output import open_loggs
from vault.datavault import DataVault
from spectrum.plotter import plot


@pytest.fixture
def data():
    real_data = (
        DataVault().input("kaon2pion"),
        DataVault().input("kaon2pion"),
    )

    mc_data = (
        (
            DataVault().input("pythia8", "kaon2pion"),
            DataVault().input("pythia8", "kaon2pion"),
        ),
        (
            DataVault().input("pythia8", "kaon2pion"),
            DataVault().input("pythia8", "kaon2pion"),
        ),
    )
    return real_data, mc_data


def reduce_func(inputs, loggs):
    fitfunc = ROOT.TF1(
        "feeddown_ratio",
        "[3] * x *(([4] + [5]) * x - [5]) + "
        "[0] * (1 + [1] * TMath::Exp(-x * x/ [2]))", 0.5, 20)
    fitfunc.SetTitle("Fit")
    fitfunc.SetLineColor(ROOT.kBlack)
    fitfunc.SetLineStyle(9)
    fitfunc.SetParameter(0, 3.109659395803652)
    fitfunc.SetParameter(1, -0.39094679433665736)
    fitfunc.SetParameter(2, 20.553216100613582)
    fitfunc.SetParameter(3, -0.02262708740433334)
    fitfunc.SetParameter(4, 16.09234627672746)
    fitfunc.SetParameter(5, -17.17670171607285)
    data, mc_ = inputs
    data.SetTitle(
        "Data; p_{T} (GeV/#it{c});"
        "(#frac{K^{+} + K^{-}}{#pi^{+} + #pi^{-}})^{data}"
    )
    mc_.SetTitle(
        "MC; p_{T} (GeV/#it{c});"
        "(#frac{K^{+} + K^{-}}{#pi^{+} + #pi^{-}})^{mc}"
    )
    mc = RebinTransformer(True, br.edges(data)).transform(mc_, loggs)
    # plot(
    #     # [data, mc],
    #     inputs,
    #     xlimits=(0.3, 20),
    #     ytitle="#frac{K^{+} + K^{-}}{#pi^{+} + #pi^{-}}",
    #     logy=False,
    #     logx=False,
    #     yoffset=1.6,
    # )

    double_ratio = br.ratio(data, mc)
    double_ratio.Fit(fitfunc, "RQWW")
    double_ratio.SetTitle("Double ratio")
    plot(
        [double_ratio, fitfunc],
        xlimits=(0.3, 20),
        logy=False,
        logx=True,
    )
    for i, (p, e) in enumerate(zip(*br.pars(fitfunc))):
        print("fitfunc.SetParameter({}, {})".format(i, p))
    return double_ratio


@pytest.mark.thesis
@pytest.mark.onlylocal
def test_ratio(data):
    options = DoubleK2POptions(
        data=K2POptions(
            kaons="hstat_kaon_pp13_sum",
            pions="hstat_pion_pp13_sum"
        ),
        mc=K2POptions(
            kaons=["hPt_K^{+}_", "hPt_K^{-}_"],
            pions=["hPt_#pi^{+}_", "hPt_#pi^{-}_"]
        ),
        reduce_func=reduce_func
    )

    estimator = KaonToPionDoubleRatio(options, plot=True)
    with open_loggs() as loggs:
        estimator.transform(data, loggs)
