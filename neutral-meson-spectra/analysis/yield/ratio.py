import pytest

from spectrum.corrected_yield import YieldRatio, CorrectedYield
from spectrum.options import CompositeCorrectedYieldOptions
from spectrum.output import open_loggs
from spectrum.comparator import Comparator
from tools.feeddown import data_feeddown

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
    options_eta = CompositeCorrectedYieldOptions(particle="#eta")
    options_pi0 = CompositeCorrectedYieldOptions(particle="#pi^{0}")
    # Make same binning for all neutral mesons
    options_pi0.set_binning(
        options_eta.analysis.pt.ptedges,
        options_eta.analysis.pt.rebins
    )
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

    with open_loggs("eta to pion ratio", save=False) as loggs:
        output = estimator.transform(data, loggs)
        Comparator().compare(output)


@pytest.mark.skip('Something is wrong')
def test_debug_yield_ratio(data_pion, data_eta, options):
    options_eta, options_pi0 = options

    with open_loggs("eta and pion yields", save=False) as loggs:
        eta = CorrectedYield(options_eta).transform(data_eta, loggs)
        pi0 = CorrectedYield(options_pi0).transform(data_pion, loggs)

    Comparator().compare(eta, pi0)
