import pytest
import numpy as np
import spectrum.constants as ct
from spectrum.vault import FVault
from spectrum.plotter import plot
from spectrum.spectra import energies


@pytest.fixture
def hepdata(particle):
    return energies(particle)


def tcm(spectrum, eta=0.12, particle="#pi^{0}"):
    # The formulas are taken from arXiv:1501.05235v1
    energy = spectrum.energy
    mass = ct.mass(particle)
    doublemass = 2 * 0.938
    func = FVault().tf1("tcm")
    # func = ROOT.TF1("func", "[0] * TMath::Exp(-(TMath::Sqrt(x[0] * x[0] + [5] * [5]) - [5]) / [1]) + [2] * TMath::Power(1 + x[0] * x[0] / [3] / [3] / [4], -[4])", 0, 20) # noqa
    eta_prime = eta - np.log(energy / doublemass)
    eta_prime_prime = eta + np.log(energy / doublemass)
    T = 409 * np.exp(0.06 * eta_prime_prime) * doublemass ** 0.06 / 1000
    Te = 98 * np.exp(0.06 * eta_prime_prime) * doublemass ** 0.06 / 1000
    n = 5.04 + 0.27 * eta_prime

    Aexp = 0.76 * (energy ** 2) ** 0.106
    etaexp = 0.692 + 0.293 * np.log(energy)
    sigmaexp = 0.896 + 0.136 * np.log(energy)
    expo = Aexp * (
        np.exp(- (eta - etaexp) ** 2 / 2 / sigmaexp ** 2) +
        np.exp(- (eta + etaexp) ** 2 / 2 / sigmaexp ** 2)
    )
    Apow = 0.13 * (energy ** 2) ** 0.175
    sigmapower = 0.217 + 0.235 * np.log(energy)
    power = Apow * np.exp(- eta ** 2 / 2 / sigmapower)
    Ae = 1. / 2 / Te / (mass + Te) * expo
    A = (n - 1) / n / T ** 2 * power
    func.SetParameter("n", n)
    func.SetParameter("T", T)
    func.SetParameter("Te", Te)
    func.SetParameter("Ae", Ae * 1000)
    func.SetParameter("A", A * 1000)
    func.SetParameter("M", mass)
    func.SetTitle("TCM")
    # br.report(func)
    return func


@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta",
])
def test_downloads_from_hepdata(hepdata, particle):
    for spectrum in hepdata:
        plot([spectrum, tcm(spectrum, particle=particle)])
