from __future__ import print_function
import ROOT
import pytest

from lazy_object_proxy import Proxy
from vault.datavault import DataVault
from spectrum.options import CompositeNonlinearityOptions
from spectrum.output import AnalysisOutput  # noqa
from tools.mc import Nonlinearity
from spectrum.broot import BROOT as br
from spectrum.comparator import Comparator  # noqa
# from vault.formulas import FVault

SPMC_REGULAR = Proxy(
    lambda: (
        DataVault().input("data", "nonlinearity",
                          listname="PhysPlain", histname="MassPtSM0"),
        (
            DataVault().input("single #pi^{0} new calibration", "low",
                              "PhysEff"),
            DataVault().input("single #pi^{0} new calibration", "high",
                              "PhysEff"),
        )
    )
)
# NB: This may be inactive
SPMC_NONLIN_SELECTION = Proxy(
    lambda: (
        DataVault().input("data", listname="Phys", histname="MassPt_SM0"),
        (
            DataVault().input("single #pi^{0}", "low", "PhysEff",
                              histname="MassPt_SM0"),
            DataVault().input("single #pi^{0}", "high", "PhysEff",
                              histname="MassPt_SM0"),
        )
    )
)


def nonlinearity_function():
    # func_nonlin = ROOT.TF1(
    #     "func_nonlin", FVault().func("nonlinearity"), 0, 20)
    # func_nonlin.SetParNames("A", "#sigma", "E_{scale}")

    func_nonlin = ROOT.TF1(
        "func_nonlin",
        "[2]*(1.+[0]/(1. + TMath::Power(x/[1],2)))", 0, 100)
    func_nonlin.SetParameters(-0.06, 0.7, 1.015)
    return func_nonlin


@pytest.mark.onlylocal
@pytest.mark.parametrize("data", [
    SPMC_REGULAR,
    # SPMC_NONLIN_SELECTION,
])
def test_spmc_nonlinearity(data):
    options = CompositeNonlinearityOptions()
    options.fitf = nonlinearity_function()

    nonlinearity = Nonlinearity(options, plot=True).transform(
        data, AnalysisOutput("spmc nonlinearity"))
    print("Fit parameters:", br.pars(options.fitf))
    Comparator().compare(nonlinearity)
    assert nonlinearity.GetEntries() > 0
