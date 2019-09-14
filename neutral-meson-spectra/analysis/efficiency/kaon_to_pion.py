import pytest

import ROOT

from spectrum.tools.kaon2pion import KaonToPionRatioMC
from spectrum.tools.kaon2pion import KaonToPionDoubleRatio
from spectrum.tools.kaon2pion import DoubleK2POptions, K2POptions
from spectrum.output import open_loggs
from vault.datavault import DataVault
from spectrum.comparator import Comparator


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
            DataVault().input("pythia8", "kaon2pion"),
            DataVault().input("pythia8", "kaon2pion"),
        ),
        (
            DataVault().input("pythia8", "kaon2pion"),
            DataVault().input("pythia8", "kaon2pion"),
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
