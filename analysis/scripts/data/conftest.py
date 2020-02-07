import pytest
import spectrum.broot as br
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
    return (
        DataVault().input(
            "data",
            "staging tof",
            listname="TagAndProbleTOF",
            histname="MassEnergyTOF_SM0"
        ),
        DataVault().input(
            "data",
            "staging tof",
            listname="TagAndProbleTOF",
            histname="MassEnergyAll_SM0"
        ),
    )


@pytest.fixture
def tof_data_old():
    return (
        DataVault().input(
            "data",
            "uncorrected",
            listname="TagAndProbleTOFOnlyTender",
            histname="MassEnergyTOF_SM0"),
        DataVault().input(
            "data",
            "uncorrected",
            listname="TagAndProbleTOFOnlyTender",
            histname="MassEnergyAll_SM0"
        ),
    )
