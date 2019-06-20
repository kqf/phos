import pytest
import ROOT

from vault.datavault import DataVault
from spectrum.options import NonlinearityOptions, CompositeNonlinearityOptions
from spectrum.output import open_loggs
from tools.mc import Nonlinearity


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
    return DataVault().input("data", listname="Phys", histname="MassPtSM0")


@pytest.fixture
def pythia8(data):
    return (
        data,
        DataVault().input("pythia8", listname="PhysEff", histname="MassPt"),
    )


@pytest.fixture
def spmc(data):
    return (
        data,
        (
            DataVault().input("single #pi^{0}", "low", "PhysEff",
                              histname="MassPt"),
            DataVault().input("single #pi^{0}", "high", "PhysEff",
                              histname="MassPt")
        )
    )


@pytest.mark.onlylocal
def test_simple(pythia8):
    options = NonlinearityOptions()
    options.fitf = nonlinearity_function()

    estimator = Nonlinearity(options)
    with open_loggs() as loggs:
        nonlinearity = estimator.transform(pythia8, loggs)
    assert nonlinearity.GetEntries() > 0


@pytest.mark.onlylocal
def test_composite(spmc):
    options = CompositeNonlinearityOptions()
    options.fitf = nonlinearity_function()

    estimator = Nonlinearity(options)
    with open_loggs() as loggs:
        nonlinearity = estimator.transform(spmc, loggs)
    assert nonlinearity.GetEntries() > 0
