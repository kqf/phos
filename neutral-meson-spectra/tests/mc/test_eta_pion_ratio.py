import pytest
from spectrum.comparator import Comparator
from spectrum.pipeline import SingleHistReader
from spectrum.pipeline import ComparePipeline
from spectrum.output import open_loggs
from vault.datavault import DataVault


@pytest.fixture
def data():
    return (
        DataVault().input("pythia8", histname="hPtLong_#eta"),
        DataVault().input("pythia8", histname="hPtLong_#pi^{0}"),
    )


@pytest.mark.onlylocal
@pytest.mark.interactive
def test_calculate_eta_pion_ratio(data):
    estimator = ComparePipeline([
        ("#eta", SingleHistReader()),
        ("#pi^{0}", SingleHistReader()),
    ], plot=False)
    with open_loggs("eta pion ratio generated") as loggs:
        ratio = estimator.transform(data, loggs)
        Comparator().compare(ratio)
