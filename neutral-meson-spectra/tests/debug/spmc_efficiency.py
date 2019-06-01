import pytest

from spectrum.comparator import Comparator

from spectrum.output import open_loggs
from spectrum.efficiency import Efficiency
from spectrum.options import CompositeEfficiencyOptions

from vault.datavault import DataVault


def artificial_data(self):
    inputs = (
        "LHC16-single-low.root",
        "LHC16-single.root"
    )
    return inputs


def pi0_dataset():
    inputs = (
        DataVault().input("single #eta", "low", "PhysEff"),
        DataVault().input("single #eta", "high", "PhysEff"),
    )
    return inputs


def eta_dataset():
    inputs = (
        DataVault().input("single #eta", "low"),
        DataVault().input("single #eta", "high")
    )
    return inputs


@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle, dataset", [
    ("#pi^{0}", pi0_dataset()),
    ("#eta", eta_dataset()),
])
def test_spmc_efficiency(inputs, particle):
    options = CompositeEfficiencyOptions(particle)
    # for options in options.suboptions:
    # options.analysis.signalp.relaxed = True
    # options.analysis.backgroundp.relaxed = True

    with open_loggs("composite efficiency spmc {}".format(particle)) as loggs:
        efficiency = Efficiency(options).transform(inputs, loggs)
        Comparator().compare(efficiency)
