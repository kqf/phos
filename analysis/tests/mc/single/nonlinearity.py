from __future__ import print_function
import ROOT
import pytest

from spectrum.vault import DataVault
from spectrum.options import CompositeNonlinearityOptions
from spectrum.output import open_loggs  # noqa
from spectrum.tools.mc import Nonlinearity
from spectrum.tools.mc import Decalibration
import spectrum.broot as br
from spectrum.comparator import Comparator  # noqa
from spectrum.vault import FVault


@pytest.fixture
def data():
    prod = "single #pi^{0} debug 2"
    return (
        DataVault().input("data", "latest", histname="MassPtSM0"),
        (
            DataVault().input(prod, "low", "PhysEff"),
            DataVault().input(prod, "high", "PhysEff")
        )
    )


@pytest.fixture
def nonlinearity_function_official():
    func_nonlin = ROOT.TF1(
        "func_nonlin", FVault().func("nonlinearity"), 0, 20)
    func_nonlin.SetParNames("A", "#sigma", "E_{scale}")
    func_nonlin.SetParameters(1., 0.6, 1.04)
    return func_nonlin


@pytest.fixture
def nonlinearity_function():
    func_nonlin = ROOT.TF1(
        "func_nonlin",
        "[2]*(1.+[0]/(1. + TMath::Power(x/[1],2)))", 0, 100)
    func_nonlin.SetParameters(-0.06, 0.7, 1.015)
    # func_nonlin.SetParameters(-0.04, 0.73, 1.025)
    return func_nonlin


@pytest.mark.onlylocal
@pytest.mark.interactive
def test_spmc_nonlinearity(data, nonlinearity_function):
    options = CompositeNonlinearityOptions()
    options.fitf = nonlinearity_function

    with open_loggs("spmc nonlinearity parametrization") as loggs:
        nonlinearity = Nonlinearity(options, plot=True).transform(data, loggs)
        print("Fit parameters:", br.pars(options.fitf))
        Comparator().compare(nonlinearity)

    with open_loggs("spmc width parametrization") as loggs:
        width = Decalibration(options, plot=True).transform(data, loggs)
        Comparator().compare(width)

    assert width.GetEntries() > 0
