import pytest
from spectrum.comparator import Comparator
from spectrum.pipeline import SingleHistReader
from spectrum.pipeline import ComparePipeline
from spectrum.output import open_loggs
from spectrum.vault import DataVault


@pytest.fixture
def data(etaname, pionname):
    return (
        DataVault().input("pythia8", histname=etaname),
        DataVault().input("pythia8", histname=pionname),
    )


@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("etaname, pionname", [
    ("hPtLong_#eta", "hPtLong_#pi^{0}"),
    ("hPt_#eta_primary_standard", "hPt_#pi^{0}_primary_standard"),
])
def test_calculate_eta_pion_ratio(data):
    estimator = ComparePipeline([
        ("#eta", SingleHistReader()),
        ("#pi^{0}", SingleHistReader()),
    ], plot=False)
    with open_loggs("eta pion ratio generated") as loggs:
        ratio = estimator.transform(data, loggs)
        Comparator().compare(ratio)
