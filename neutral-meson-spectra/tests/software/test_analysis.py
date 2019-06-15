import pytest

from spectrum.output import AnalysisOutput
from spectrum.options import Options, CompositeOptions
from spectrum.analysis import Analysis
from vault.datavault import DataVault

from spectrum.comparator import Comparator


@pytest.fixture
def data():
    return DataVault().input("data", histname="MassPtSM0")


@pytest.fixture
def data_spmc():
    return (
        DataVault().input("single #pi^{0}", "low", "PhysEff"),
        DataVault().input("single #pi^{0}", "high", "PhysEff"),
    )


@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    # "#eta",
])
def test_simple(particle, data):
    analysis = Analysis(Options(particle=particle))
    loggs = AnalysisOutput("test the single analysis")
    output = analysis.transform(data, loggs=loggs)
    # loggs.plot()
    Comparator().compare(output.spectrum)
    assert len(output) > 0


@pytest.mark.skip("")
@pytest.mark.interactive
@pytest.mark.onlylocal
def test_composite(data_spmc):
    analysis = Analysis(CompositeOptions("#pi^{0}"))
    loggs = AnalysisOutput("test the composite analysis")
    output = analysis.transform(data_spmc, loggs=loggs)
    # loggs.plot()
    assert len(output) > 0
