import ROOT
import pytest
from spectrum.spectra import spectrum
from spectrum.plotter import plot
from vault.formulas import FVault
import spectrum.broot as br


@pytest.fixture
def pion():
    pion = spectrum("#pi^{0}")
    pion.SetTitle("#pi^{0}")
    return pion


@pytest.fixture
def eta():
    eta = spectrum("#eta")
    eta.SetTitle("#eta")
    return eta


@pytest.fixture
def pionf():
    pionf = FVault().tf1("tcm", "#pi^{0} 13 TeV")
    pionf.SetTitle("#pi^{0}, TCM")
    return pionf


@pytest.fixture
def eta_mtf(pionf):
    eta_mtf = ROOT.TF1("eta_mtf", lambda x,
                       p: pionf.Eval(x[0]) * p[0], 2, 20, 1)
    eta_mtf.SetParameter(0, 0.5)
    eta_mtf.SetTitle("m_{T} scaled")
    return eta_mtf


@pytest.mark.thesis
@pytest.mark.onlylocal
def test_spectrum(pion, eta, pionf, eta_mtf):
    eta.Fit(eta_mtf, "R")
    plot([
        pion,
        eta,
        pionf,
        eta_mtf,
    ])

    plot([
        br.ratio(pion, br.function2histogram(pionf, pion)),
        br.ratio(eta, br.function2histogram(eta_mtf, eta)),
    ], ylimits=(0, 1.2), logy=False)
