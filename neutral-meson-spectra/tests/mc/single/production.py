import pytest

from vault.datavault import DataVault
from spectrum.options import CompositeNonlinearityOptions
from tools.mc import Nonlinearity, Decalibration, Shape
from spectrum.output import open_loggs


@pytest.fixture
def data():
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


@pytest.mark.parametrize("method", [
    Nonlinearity,
    Decalibration,
    Shape
])
def test_calculate_quantities(method, data):
    options = CompositeNonlinearityOptions("#pi^{0}")
    options.fitf = None
    with open_loggs("spmc production check") as loggs:
        nonlin = method(options).transform(data, loggs)
    assert nonlin.GetEntries() > 0
