import pytest
from spectrum.spectra import spectrum, ratio
from spectrum.comparator import Comparator
from vault.formulas import FVault
from spectrum.broot import BROOT as br


@pytest.mark.thesis
@pytest.mark.onlylocal
def test_spectrum():
    pion = spectrum("#pi^{0}")
    pion.logy = True
    pion.logx = True
    eta = spectrum("#eta")
    eta.logy = True
    eta.lox = True
    eta.label = "#eta"

    mtscaled = FVault().tf1("tsallis", "#pi^{0} 13 TeV")
    for i in range(1, mtscaled.GetNpar()):
        mtscaled.FixParameter(i, mtscaled.GetParameter(i))

    mtscaled.SetRange(2.2, 20)
    eta.Fit(mtscaled, "R")
    Comparator().compare(pion, eta)

    fitf = FVault().tf1("tsallis", "#eta 13 TeV")
    for i in range(1, fitf.GetNpar()):
        fitf.FixParameter(i, fitf.GetParameter(i))
        fitf.SetRange(0, 20)
    pion.Fit(fitf, "R")

    original_tsallis = FVault().tf1("tsallis", "#pi^{0} 13 TeV")
    pion_param = Comparator().compare(
        pion, br.function2histogram(original_tsallis, pion))

    eta_mtscaled = Comparator().compare(
        eta, br.function2histogram(mtscaled, eta))

    Comparator().compare(pion_param, eta_mtscaled)
    eta_pion_mtscaled = Comparator().compare(
        eta,
        br.function2histogram(fitf, eta)
    )

    Comparator().compare(eta_pion_mtscaled, ratio(stop=False))
