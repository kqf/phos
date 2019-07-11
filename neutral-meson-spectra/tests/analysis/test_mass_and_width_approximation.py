import ROOT
import pytest

from spectrum.output import open_loggs
from spectrum.options import Options
from spectrum.analysis import Analysis
from vault.datavault import DataVault
from spectrum.comparator import Comparator


def fit_quantity(quantity, formula):
    ROOT.gStyle.SetOptFit(1)
    fitf = ROOT.TF1("fitf", formula)
    quantity.Fit(fitf)
    quantity.SetLineColor(ROOT.kRed + 1)
    Comparator().compare(quantity)


@pytest.fixture
def data():
    return DataVault().input("data", histname="MassPtSM0")


@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta"]
)
def test_mass_width_parametrization(particle, data):
    options = Options(particle=particle)
    with open_loggs("test mass width parameters") as loggs:
        output = Analysis(options).transform(data, loggs)

    fit_quantity(output.mass, options.calibration.mass_func)
    fit_quantity(output.width, options.calibration.width_func)
