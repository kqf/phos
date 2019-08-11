import pytest

from spectrum.output import open_loggs
from spectrum.options import Options
from spectrum.analysis import Analysis
from vault.datavault import DataVault


@pytest.fixture
def data():
    return DataVault().input("data", listname="Phys3", histname="MassPtSM0")


@pytest.mark.onlylocal
@pytest.mark.interactive
def test_parameters_for_acceptance_calculation(data):
    analysis = Analysis(Options(particle="#pi^{0}"))
    with open_loggs("test acceptance params") as loggs:
        output = analysis.transform(data, loggs=loggs)
    assert len(output) > 0
