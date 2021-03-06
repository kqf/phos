import ROOT
import pytest
import numpy as np

import spectrum.plotter as plt

from spectrum.spectra import spectrum, ratio
from spectrum.constants import mass
from spectrum.constants import invariant_cross_section_code
from spectrum.vault import FVault
import spectrum.broot as br
import pandas as pd


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
@pytest.mark.parametrize("target", [""])
def test_spectrum(pion, eta, pionf, eta_mtf, coname, target):
    eta.Fit(eta_mtf, "R0Q")
    plt.plot([
        pion,
        eta,
        pionf,
        eta_mtf,
    ],
        xtitle="#it{p}_{T} (GeV/#it{c})",
        ytitle=invariant_cross_section_code(),
        oname=coname.format("mt_scaling/fits")
    )

    plt.plot([
        tcmratio(pionf, pion, "TCM-fit"),
        tcmratio(eta_mtf, eta, "#it{m}_{T} scaled TCM-fit"),
    ],
        xlimits=(0.8, 20.0),
        ylimits=(0, 3.4),
        logy=False,
        ytitle="Data / TCM fit",
        xtitle="#it{p}_{T} (GeV/#it{c})",
        legend_pos=(0.4, 0.7, 0.7, 0.85),
        oname=coname.format("mt_scaling/ratio")
    )


def mt(particle, momentum):
    return (mass(particle) ** 2 + momentum ** 2) ** 0.5


def eta_pion_ratio(x, par):
    c, a, n = par
    numerator = a + mt("#eta", x[0])
    denominator = a + mt("#pi^{0}", x[0])
    return c * (numerator / denominator) ** -n


@pytest.fixture
def asymptotic_value_eta_pion_ratio(eta_pion_ratio_fitf):
    rratio = ratio(stop=False)
    rratio.Fit(eta_pion_ratio_fitf, "R")
    etapion = eta_pion_ratio_fitf.GetParameter(0)
    etapione = eta_pion_ratio_fitf.GetParError(0)
    print()
    print("Asymptotic #eta / #pi^{0} ratio: ", etapion, etapione)
    return etapion


@pytest.fixture
def upper(asymptotic_value_eta_pion_ratio):
    upper = ROOT.TF1("upper", eta_pion_ratio, 0, 20, 3)
    upper.SetParameter(0, asymptotic_value_eta_pion_ratio)
    upper.SetParameter(1, 1.2)
    upper.SetParameter(2, 10)
    return upper


@pytest.fixture
def lower():
    lower = ROOT.TF1("lower", eta_pion_ratio, 0, 20, 3)
    lower.SetParameter(0, 0.436)
    lower.SetParameter(1, 1.2)
    lower.SetParameter(2, 14)
    return lower


@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.parametrize("target", ["mt_scaling/eta_pion_ratio"])
def test_ratio(upper, lower, coname, target):
    plt.plot([
        ratio(stop=False),
        br.shaded_region("#it{m}_{T} scaling", lower, upper),
    ],
        logy=False,
        logx=False,
        ytitle="#eta / #pi^{0}",
        xtitle="#it{p}_{T} (GeV/#it{c})",
        csize=plt.wide_csize,
        tmargin=0.01,
        rmargin=0.01,
        lmargin=0.1,
        yoffset=1.,
        legend_pos=(0.6, 0.2, 0.8, 0.35),
        options=["p", "f"],
        oname=coname.format(""),
    )


@pytest.mark.thesis
@pytest.mark.onlylocal
def test_mt_deviation(upper, lower, pt_cut=6.5):
    etapion = br.bins(ratio(stop=False))
    idx = etapion.centers > pt_cut
    values, errors = etapion.contents[idx], etapion.errors[idx]
    exp, sigma = br.weighted_avg_and_std(values, errors)
    print("Eta/pion weighted mean {:.3g} #pm {:.3g}".format(exp, sigma))

    print(
        pd.DataFrame({
            "pT": etapion.centers[idx],
            "eta/pion": values,
            "eta/pion errors": errors
        }).to_string(index=False)
    )

    theory_upper = upper.Eval(etapion.centers[idx].mean())
    print("Theory upper", theory_upper)
    assert exp - 2 * sigma < theory_upper < exp + 2 * sigma

    theory_lower = lower.Eval(etapion.centers[idx].mean())
    print("Theory lower", theory_lower)
    assert exp - 2 * sigma < theory_lower < exp + 2 * sigma


@pytest.fixture
def ndof():
    return 3


@pytest.mark.thesis
@pytest.mark.onlylocal
def test_chi2(upper, lower, ndof):
    etapion = br.bins(ratio(stop=False))
    values, errors = etapion.contents, etapion.errors
    pT = etapion.centers

    theory_upper = np.vectorize(upper.Eval)(pT)
    theory_lower = np.vectorize(lower.Eval)(pT)

    df = pd.DataFrame({
        "pT": etapion.centers,
        "eta/pion": values,
        "eta/pion errors": errors,
        "upper": theory_upper,
        "lower": theory_lower,
    })

    df["(D - E) / S (upper)"] = (
        (df["eta/pion"] - df["upper"]) / df["eta/pion errors"])

    df["(D - E) / S (lower)"] = (
        (df["eta/pion"] - df["lower"]) / df["eta/pion errors"])

    df["chi2 (upper)"] = df["(D - E) / S (upper)"] ** 2
    df["chi2 (lower)"] = df["(D - E) / S (lower)"] ** 2

    chi2_upper = (df["chi2 (upper)"].sum())
    chi2_lower = (df["chi2 (lower)"].sum())

    print("chi^2 (upper) {:.4g} chi^2 (bottom) {:.4g}".format(
        chi2_upper,
        chi2_lower,
    ))

    print("chi^2/n (upper) {:.4g} chi^2 /n (bottom) {:.4g}".format(
        chi2_upper / (len(df) - ndof),
        chi2_lower / (len(df) - ndof),
    ))

    print(df.to_string(index=False))
