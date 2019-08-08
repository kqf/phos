import pytest

from spectrum.corrected_yield import YieldRatio, CorrectedYield
from spectrum.options import CompositeCorrectedYieldOptions
from spectrum.output import open_loggs
from spectrum.comparator import Comparator
from spectrum.tools.feeddown import data_feeddown

from vault.datavault import DataVault


@pytest.fixture
def data_eta():
    # Define the inputs and the dataset for #eta mesons
    #

    inputs_eta = (
        DataVault().input("single #eta", "low", "PhysEff"),
        DataVault().input("single #eta", "high", "PhysEff"),
    )

    data = (
        (
            DataVault().input("data", histname="MassPtSM0"),
            data_feeddown(dummy=True),
        ),
        inputs_eta
    )
    return data


@pytest.fixture
def data_pion():
    # Define the inputs and the dataset for #pi^{0}
    #
    prod = "single #pi^{0}"
    inputs_pi0 = (
        DataVault().input(prod, "low", "PhysEff"),
        DataVault().input(prod, "high", "PhysEff"),
    )

    data = (
        (
            DataVault().input("data", histname="MassPtSM0"),
            data_feeddown(),
        ),
        inputs_pi0
    )

    return data


@pytest.fixture
def data(data_eta, data_pion):
    return data_eta, data_pion


@pytest.fixture
def options():
    pt = "config/pt-same.json"
    options_eta = CompositeCorrectedYieldOptions(particle="#eta", pt=pt)
    options_pi0 = CompositeCorrectedYieldOptions(particle="#pi^{0}", pt=pt)
    return options_eta, options_pi0


@pytest.mark.onlylocal
@pytest.mark.interactive
def test_yield_ratio(data, options):
    options_eta, options_pi0 = options

    estimator = YieldRatio(
        options_eta=options_eta,
        options_pi0=options_pi0,
        plot=True
    )

    with open_loggs("eta to pion ratio") as loggs:
        output = estimator.transform(data, loggs)
        Comparator().compare(output)


@pytest.mark.skip("ignore")
@pytest.mark.onlylocal
@pytest.mark.interactive
def test_debug_yield_ratio(data_pion, data_eta):
    with open_loggs() as loggs:
        eta = CorrectedYield(
            CompositeCorrectedYieldOptions(particle="#eta")
        ).transform(data_eta, loggs)

        pi0 = CorrectedYield(
            CompositeCorrectedYieldOptions(particle="#pi^{0}")
        ).transform(data_pion, loggs)

    Comparator(rrange=(-1,)).compare(eta, pi0)
