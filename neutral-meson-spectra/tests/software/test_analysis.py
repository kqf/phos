import pytest

from lazy_object_proxy import Proxy
from spectrum.output import AnalysisOutput
from spectrum.options import Options, CompositeOptions
from spectrum.analysis import Analysis
from vault.datavault import DataVault

from spectrum.comparator import Comparator

INPUT_DATA = Proxy(
    lambda: DataVault().input("data", histname="MassPtSM0")
)

SPMC_DATA = Proxy(
    lambda: (
        DataVault().input("single #pi^{0}", "low", "PhysEff"),
        DataVault().input("single #pi^{0}", "high", "PhysEff"),
    )
)


@pytest.mark.onlylocal
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    # "#eta",
])
def test_simple(particle):
    analysis = Analysis(Options(particle=particle))
    loggs = AnalysisOutput("test the single analysis")
    output = analysis.transform(INPUT_DATA, loggs=loggs)
    # loggs.plot()
    Comparator().compare(output.spectrum)
    assert len(output) > 0


@pytest.mark.skip("")
@pytest.mark.onlylocal
def test_composite():
    analysis = Analysis(CompositeOptions("#pi^{0}"))
    loggs = AnalysisOutput("test the composite analysis")
    output = analysis.transform(SPMC_DATA, loggs=loggs)
    # loggs.plot()
    assert len(output) > 0
