import ROOT
import pytest
from spectrum.spectra import spectrum, ratio
from spectrum.plotter import plot
from spectrum.constants import mass
import spectrum.sutils as su
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


def tcmratio(func, hist, title):
    histratio = br.ratio(hist, br.function2histogram(func, hist))
    histratio.SetTitle("{}, data / {}".format(hist.GetTitle(), title))
    return histratio


@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.skip("")
def test_spectrum(pion, eta, pionf, eta_mtf):
    eta.Fit(eta_mtf, "R")
    plot([
        pion,
        eta,
        pionf,
        eta_mtf,
    ])

    plot([
        tcmratio(pionf, pion, "TCM-fit"),
        tcmratio(eta_mtf, eta, "m_{T}-scaled TCM-fit"),
    ],
        xlimits=(0.8, 20.0), ylimits=(0, 3.4), logy=False,
        ytitle="Data / TCM fit"
    )


def mt(particle, momentum):
    return (mass(particle) ** 2 + momentum ** 2) ** 0.5


def eta_pion_ratio(x, par):
    c, a, n = par
    numerator = a + mt("#eta", x[0])
    denominator = a + mt("#pi^{0}", x[0])
    return c * (numerator / denominator) ** -n


@pytest.mark.thesis
@pytest.mark.onlylocal
def test_ratio():
    lower = ROOT.TF1("lower", eta_pion_ratio, 0, 16, 3)
    lower.SetParameter(0, 0.436)
    lower.SetParameter(1, 1.2)
    lower.SetParameter(2, 10)

    upper = ROOT.TF1("upper", eta_pion_ratio, 0, 16, 3)
    upper.SetParameter(0, 0.436)
    upper.SetParameter(1, 1.2)
    upper.SetParameter(2, 14)
    plot([
        ratio(stop=False),
        br.shaded_region("m_{T}-scaling", upper, lower),
    ],
        logy=False,
        logx=False
    )
