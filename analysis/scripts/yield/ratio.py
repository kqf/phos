import pytest

from spectrum.cyield import YieldRatio
from spectrum.cyield import cyield_data
from spectrum.options import CompositeCorrectedYieldOptions
from spectrum.output import open_loggs
from spectrum.comparator import Comparator


@pytest.fixture
def data():
    return cyield_data("#eta"), cyield_data("#pi^{0}")


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

    with open_loggs("debug eta pion ratio") as loggs:
        output = estimator.transform(data, loggs)
        Comparator().compare(output)
