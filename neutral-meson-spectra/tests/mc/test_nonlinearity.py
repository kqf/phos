import pytest
import ROOT

from vault.datavault import DataVault
from spectrum.options import NonlinearityOptions
from spectrum.output import AnalysisOutput
from tools.mc import Nonlinearity


def nonlinearity_function():
    func_nonlin = ROOT.TF1(
        "func_nonlin",
        "[2] * (1.+[0]*TMath::Exp(-x/2*x/2/2./[1]/[1]))",
        0, 100
    )
    func_nonlin.SetParNames('A', '#sigma', 'E_{scale}')
    func_nonlin.SetParameter(0, -0.05)
    func_nonlin.SetParameter(1, 0.6)
    func_nonlin.SetParLimits(1, 0, 10)
    func_nonlin.SetParameter(2, 1.04)
    return func_nonlin


@pytest.mark.onlylocal
def test_calculate_nonlinearity():
    options = NonlinearityOptions()
    options.fitf = nonlinearity_function()

    estimator = Nonlinearity(options, plot=True)
    nonlinearity = estimator.transform(
        (
            DataVault().input('data', listname="Phys",
                              histname="MassPtSM0"),
            DataVault().input('pythia8', listname="PhysEff",
                              histname="MassPt"),
        ),
        loggs=AnalysisOutput("calculate the nonlinearity")
    )
    assert nonlinearity.GetEntries() > 0
