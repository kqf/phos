import pytest
import ROOT

from vault.datavault import DataVault
from spectrum.options import NonlinearityOptions
from spectrum.output import open_loggs
from tools.mc import Nonlinearity
from spectrum.comparator import Comparator


def nonlinearity_function():
    func_nonlin = ROOT.TF1(
        "func_nonlin",
        "[2] * (1.+[0]*TMath::Exp(-x/2*x/2/2./[1]/[1]))",
        0, 100
    )
    func_nonlin.SetParNames("A", "#sigma", "E_{scale}")
    func_nonlin.SetParameter(0, -0.05)
    func_nonlin.SetParameter(1, 0.6)
    func_nonlin.SetParLimits(1, 0, 10)
    func_nonlin.SetParameter(2, 1.04)
    return func_nonlin


@pytest.fixture
def data():
    return (
        DataVault().input("data", listname="Phys", histname="MassPtSM0"),
        DataVault().input("pythia8", listname="PhysEff", histname="MassPt"),
    )


@pytest.mark.onlylocal
@pytest.mark.interactive
def test_calculate_nonlinearity(data):
    options = NonlinearityOptions()
    options.fitf = nonlinearity_function()

    estimator = Nonlinearity(options, plot=True)
    with open_loggs("nonlinearity") as loggs:
        nonlinearity = estimator.transform(data, loggs)
        Comparator().compare(nonlinearity)

    assert nonlinearity.GetEntries() > 0
