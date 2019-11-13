import ROOT
import pytest

import spectrum.broot as br
from spectrum.output import open_loggs
from spectrum.options import Options
from spectrum.analysis import Analysis
from vault.datavault import DataVault
from spectrum.plotter import plot


def fit(hist, quant, particle):
    hist.SetTitle("Data")
    bins = br.edges(hist)
    fitf = ROOT.TF1(hist.GetName(), quant.func, min(bins), max(bins))
    fitf.SetTitle("Fit")
    fitf.SetLineColor(ROOT.kBlack)
    fitf.SetLineStyle(9)
    for i, p in enumerate(quant.pars):
        fitf.SetParameter(i, p)
    hist.Fit(fitf, "Q")
    br.report(fitf, particle)
    plot([hist, fitf], logy=False)


@pytest.fixture
def data():
    return DataVault().input("data", histname="MassPtSM0")


@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta"
])
def test_mass_width_parametrization(particle, data):
    options = Options(particle=particle)
    with open_loggs("test mass width parameters") as loggs:
        output = Analysis(options).transform(data, loggs)

    fit(output.mass, options.calibration.mass, particle)
    fit(output.width, options.calibration.width, particle)
