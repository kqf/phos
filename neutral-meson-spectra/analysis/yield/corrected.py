import pytest  # noqa

from spectrum.options import CompositeCorrectedYieldOptions
from spectrum.corrected_yield import CorrectedYield
from spectrum.output import open_loggs

from vault.datavault import DataVault
from spectrum.tools.feeddown import data_feeddown


def pion_data():
    return (
        (
            DataVault().input("data", histname="MassPtSM0"),
            data_feeddown(),
        ),
        (
            DataVault().input("single #pi^{0}", "low", "PhysEff"),
            DataVault().input("single #pi^{0}", "high", "PhysEff"),
        )
    )


def eta_data():
    return (
        (
            DataVault().input("data", histname="MassPtSM0"),
            data_feeddown(dummy=True)
        ),
        (
            DataVault().input("single #eta", "low"),
            DataVault().input("single #eta", "high"),
        )
    )


@pytest.fixture
def data(particle):
    return {
        "#pi^{0}": pion_data(),
        "#eta": eta_data(),

    }.get(particle)


@pytest.mark.interactive
@pytest.mark.parametrize("particle", [
    # "#pi^{0}",
    "#eta",
])
def test_corrected_yield_for_pi0(particle, data):
    with open_loggs("corrected yield {}".format(particle)) as loggs:
        estimator = CorrectedYield(
            CompositeCorrectedYieldOptions(
                particle=particle
            )
        )
        estimator.transform(data, loggs)
