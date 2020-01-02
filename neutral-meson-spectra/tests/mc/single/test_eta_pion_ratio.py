import pytest
from spectrum.pipeline import SingleHistReader
from spectrum.pipeline import ComparePipeline
from spectrum.output import open_loggs
from vault.datavault import DataVault


@pytest.fixture
def data(selection, production="single #pi^{0}"):
    return (
        DataVault().input(production, selection,
                          listname="PhysEff", histname="hPtLong_#eta"),
        DataVault().input(production, selection,
                          listname="PhysEff", histname="hPtLong_#pi^{0}"),
    )


@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("selection", [
    "low",
    "high",
])
def test_calculate_eta_pion_ratio(data):
    estimator = ComparePipeline([
        ("#eta", SingleHistReader()),
        ("#pi^{0}", SingleHistReader()),
    ], plot=True)

    with open_loggs("eta pion ratio generated") as loggs:
        estimator.transform(data, loggs)
