import pytest

from vault.datavault import DataVault
from spectrum.options import CompositeNonlinearityOptions
from tools.mc import Nonlinearity, Decalibration, Shape
from spectrum.output import AnalysisOutput


def define_inputs():
    production = "single #pi^{0}"
    listname = "PhysEff"
    histname = "MassPt"
    data = DataVault().input("data", listname="Phys", histname="MassPtSM0")
    mc_inputs = (
        DataVault().input(production, "low",
                          listname=listname,
                          histname=histname),
        DataVault().input(production, "high",
                          listname=listname,
                          histname=histname)
    )
    return data, mc_inputs


@pytest.mark.parametrize("method", [Nonlinearity, Decalibration, Shape])
def test_calculate_quantities(method):
    name = method.__class__.__name__.lower()
    options = CompositeNonlinearityOptions("#pi^{0}")
    options.fitf = None
    nonlin = method(options).transform(
        define_inputs(),
        loggs=AnalysisOutput("spmc {}".format(name))
    )
    assert nonlin.GetEntries() > 0
