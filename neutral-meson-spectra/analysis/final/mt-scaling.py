import pytest
from spectrum.spectra import spectrum, ratio
from spectrum.comparator import Comparator
from spectrum.plotter import plot
from vault.formulas import FVault
import spectrum.broot as br


@pytest.mark.thesis
@pytest.mark.onlylocal
def test_spectrum():
    pion = spectrum("#pi^{0}")
    pion.logy = True
    pion.logx = True
    pion.SetTitle("#pi^{0}")
    eta = spectrum("#eta")
    eta.logy = True
    eta.lox = True
    eta.label = "#eta"
    eta.SetTitle("#eta")

    mtscaled = FVault().tf1("tsallis", "#pi^{0} 13 TeV", fixed=True)
    mtscaled.SetParameter(0, mtscaled.GetParameter(0))
    mtscaled.SetRange(2.2, 20)
    eta.Fit(mtscaled, "R")
    plot([pion, eta])

    fitf = FVault().tf1("tsallis", "#eta 13 TeV", fixed=True)
    fitf.SetParameter(0, mtscaled.GetParameter(0))
    pion.Fit(fitf, "R")

    original_tsallis = FVault().tf1("tsallis", "#pi^{0} 13 TeV")
    pion_param = Comparator(stop=False).compare(
        pion, br.function2histogram(original_tsallis, pion))

    eta_mtscaled = Comparator(stop=False).compare(
        eta, br.function2histogram(mtscaled, eta))
    eta_mtscaled.SetTitle("#eta m_{T}-scaled")

    plot([pion_param, eta_mtscaled])
    eta_pion_mtscaled = Comparator(stop=False).compare(
        eta,
        br.function2histogram(fitf, eta)
    )

    plot([eta_pion_mtscaled, ratio(stop=False)])
