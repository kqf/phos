import ROOT
import pytest

from spectrum.output import AnalysisOutput
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


@pytest.mark.interactive
@pytest.mark.onlylocal
@pytest.mark.parametrize("particle", ["#pi^{0}", "#eta"])
def test_mass_width_parametrization(particle):
    options = Options(particle=particle)
    output = Analysis(options).transform(
        DataVault().input("data", histname="MassPtSM0"),
        loggs=AnalysisOutput("test the single analysis")
    )

    fit_quantity(output.mass, options.spectrum.mass_func)
    fit_quantity(output.width, options.spectrum.width_func)