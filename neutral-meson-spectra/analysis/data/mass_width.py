import ROOT
import pytest

import spectrum.broot as br
from spectrum.output import open_loggs
from spectrum.options import Options
from spectrum.analysis import Analysis
from vault.datavault import DataVault
from spectrum.plotter import plot


def fit_quantity(quantity, quant):
    ROOT.gStyle.SetOptFit(1)
    bins = br.bins(quantity).centers
    fitf = ROOT.TF1("Fit", quant.func, min(bins), max(bins))
    fitf.SetTitle("Fit")
    for i, p in enumerate(quant.pars):
        fitf.FixParameter(i, p)
    quantity.Fit(fitf, "Q")
    quantity.SetLineColor(ROOT.kRed + 1)
    plot([quantity, fitf], logy=False)


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

    fit_quantity(output.mass, options.calibration.mass)
    fit_quantity(output.width, options.calibration.width)
