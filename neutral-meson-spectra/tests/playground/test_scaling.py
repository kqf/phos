import pytest

from lazy_object_proxy import Proxy
from spectrum.output import AnalysisOutput
from spectrum.options import Options
from spectrum.analysis import Analysis
from vault.datavault import DataVault

from spectrum.comparator import Comparator

INPUT_DATA = Proxy(
    lambda: DataVault().input("data", histname="MassPtSM0")
)


def scale_data(data, scale=2):
    real, mixed = data.transform()
    real.Scale(scale)

    class ScaledInput(object):
        def transform(self):
            return (real, mixed)
    return ScaledInput()


@pytest.mark.onlylocal
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta",
])
def test_simple(particle):
    loggs = AnalysisOutput("test the single analysis")

    original = Analysis(Options(particle=particle)).transform(
        INPUT_DATA, loggs=loggs)

    scaled = Analysis(Options(particle=particle)).transform(
        scale_data(INPUT_DATA), loggs=loggs)

    Comparator().compare(original, scaled)
