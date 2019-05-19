import pytest
from tqdm import trange

from spectrum.options import (CompositeNonlinearityScanOptions,
                              NonlinearityScanOptions)
from spectrum.output import AnalysisOutput
from tools.scan import NonlinearityScan
from vault.datavault import DataVault


@pytest.fixture
def nbins():
    return 2


# TODO: Add interface for nonlinearity scan
@pytest.mark.onlylocal
@pytest.mark.skip("Don't do nonlinearity scan for pythia8")
def test_interface(nbins):
    nbins = 2
    estimator = NonlinearityScan(
        NonlinearityScanOptions(nbins=nbins)
    )

    mc = [
        DataVault().input(
            "pythia8",
            listname="PhysNonlinScan",
            histname="MassPt_{}_{}".format(i, j)
        )
        for j in trange(nbins) for i in trange(nbins)
    ]

    assert estimator.transform(
        (DataVault().input("data", histname="MassPtSM0"), mc),
        loggs=AnalysisOutput("testing the scan interface")
    )


@pytest.mark.onlylocal
def test_composite_interface(nbins):
    prod = "single #pi^{0}"
    histnames = sum([
        [
            "hMassPt_{}_{}".format(i, j),
            "hMixMassPt_{}_{}".format(i, j),
        ]
        for j in range(nbins)
        for i in range(nbins)
    ], [])

    low = DataVault().input(prod, "low", inputs=histnames)
    high = DataVault().input(prod, "high", inputs=histnames)

    estimator = NonlinearityScan(
        CompositeNonlinearityScanOptions(nbins=nbins)
    )

    low, high = low.read_multiple(2), high.read_multiple(2)
    mc_data = [(l, h) for l, h in zip(low, high)]

    assert estimator.transform(
        (DataVault().input("data", histname="MassPtSM0"), mc_data),
        loggs=AnalysisOutput("testing the scan interface")
    )
