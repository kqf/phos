import pytest
import spectrum.broot as br
from spectrum.tools.probe import tof_data as tdata
from spectrum.vault import DataVault


@pytest.fixture
def ltitle(particle):
    return "{} #rightarrow #gamma #gamma".format(particle)


@pytest.fixture
def data():
    return DataVault().input("data", histname="MassPtSM0")


@pytest.fixture
def oname(particle, target):
    target = target.replace("cball_", "")
    pattern = "images/analysis/data/{}_{}.pdf"
    return pattern.format(target, br.spell(particle))


@pytest.fixture
def tof_data():
    return tdata()
