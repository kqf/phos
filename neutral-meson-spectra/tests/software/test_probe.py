import pytest

from tools.probe import TagAndProbe
from vault.datavault import DataVault
from spectrum.options import ProbeTofOptions
from spectrum.output import open_loggs


@pytest.fixture
def data():
    return (
        DataVault().input("data", listname="TagAndProbleTOF",
                          histname="MassEnergyTOF_SM0"),
        DataVault().input("data", listname="TagAndProbleTOF",
                          histname="MassEnergyAll_SM0"),
    )


@pytest.mark.onlylocal
def test_interface(data):
    probe = TagAndProbe(ProbeTofOptions())

    with open_loggs() as loggs:
        eff = probe.transform(data, loggs)

    assert eff.GetEntries() > 0
