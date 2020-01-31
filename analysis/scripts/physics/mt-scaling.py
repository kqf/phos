import ROOT
import pytest
from spectrum.spectra import spectrum, ratio
from spectrum.plotter import plot
from spectrum.constants import mass
from spectrum.constants import invariant_cross_section_code
from spectrum.vault import FVault
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
    pionf.SetLineColor(ROOT.kBlack)
    return pionf


@pytest.fixture
def eta_mtf(pionf):
    eta_mtf = ROOT.TF1("eta_mtf", lambda x,
                       p: pionf.Eval(x[0]) * p[0], 2, 20, 1)
    eta_mtf.SetParameter(0, 0.5)
    eta_mtf.SetTitle("#it{m}_{T} scaled")
    eta_mtf.SetLineColor(ROOT.kBlack)
    eta_mtf.SetLineStyle(7)
    return eta_mtf


def tcmratio(func, hist, title):
    histratio = br.ratio(hist, func)
    histratio.SetTitle("{}, data / {}".format(hist.GetTitle(), title))
    return histratio


@pytest.mark.thesis
@pytest.mark.onlylocal
def test_spectrum(pion, eta, pionf, eta_mtf):
    eta.Fit(eta_mtf, "R0Q")
    plot([
        pion,
        eta,
        pionf,
        eta_mtf,
    ],
        xlimits=(0.8, 20.0),
        xtitle="#it{p}_{T} (GeV/#it{c})",
        ytitle=invariant_cross_section_code(),
        csize=(96, 128),
        oname="results/discussion/mt_scaling/fits.pdf"
    )

    plot([
        tcmratio(pionf, pion, "TCM-fit"),
        tcmratio(eta_mtf, eta, "#it{m}_{T} scaled TCM-fit"),
    ],
        xlimits=(0.8, 20.0),
        ylimits=(0, 3.4),
        logy=False,
        ytitle="Data / TCM fit",
        xtitle="#it{p}_{T} (GeV/#it{c})",
        csize=(96, 128),
        legend_pos=(0.45, 0.7, 0.75, 0.85),
        oname="results/discussion/mt_scaling/ratio.pdf"
    )


def mt(particle, momentum):
    return (mass(particle) ** 2 + momentum ** 2) ** 0.5


def eta_pion_ratio(x, par):
    c, a, n = par
    numerator = a + mt("#eta", x[0])
    denominator = a + mt("#pi^{0}", x[0])
    return c * (numerator / denominator) ** -n


@pytest.fixture(scope="module")
def asymptotic_eta_pion_ratio(min_pt=5):
    rratio = ratio(stop=False)
    fitf = ROOT.TF1("eta_pion", "[0]", min_pt, 20)
    rratio.Fit(fitf, "R")
    etapion = fitf.GetParameter(0)
    print()
    print("Asymptotic #eta / #pi^{0} ratio: ", etapion)
    return etapion


@pytest.mark.thesis
@pytest.mark.onlylocal
def test_ratio(asymptotic_eta_pion_ratio):
    lower = ROOT.TF1("lower", eta_pion_ratio, 0, 20, 3)
    lower.SetParameter(0, asymptotic_eta_pion_ratio)
    lower.SetParameter(1, 1.2)
    lower.SetParameter(2, 10)

    upper = ROOT.TF1("upper", eta_pion_ratio, 0, 20, 3)
    upper.SetParameter(0, 0.436)
    upper.SetParameter(1, 1.2)
    upper.SetParameter(2, 14)
    plot([
        ratio(stop=False),
        br.shaded_region("#it{m}_{T} scaling", upper, lower),
    ],
        logy=False,
        logx=False,
        csize=(96 * 1.5, 96),
        ytitle="#eta / #pi^{0}",
        xtitle="#it{p}_{T} (GeV/#it{c})",
        options=["p", "f"],
        oname="results/discussion/mt_scaling/eta_pion_ratio.pdf",
    )
