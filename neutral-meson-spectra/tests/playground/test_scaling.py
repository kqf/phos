import pytest

from spectrum.output import open_loggs
from spectrum.options import Options
from spectrum.analysis import Analysis
from vault.datavault import DataVault

from spectrum.comparator import Comparator


@pytest.fixture
def data():
    return DataVault().input("data", histname="MassPtSM0")


def scale_data(data, scale=2):
    real, mixed = data.transform()
    real.Scale(scale)

    class ScaledInput(object):
        def transform(self):
            return (real, mixed)
    return ScaledInput()


@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta",
])
def test_simple(particle, data):

    with open_loggs("test the single analysis") as loggs:
        original = Analysis(Options(particle=particle)).transform(
            data, loggs)

        scaled = Analysis(Options(particle=particle)).transform(
            scale_data(data), loggs)

    Comparator().compare(original, scaled)
