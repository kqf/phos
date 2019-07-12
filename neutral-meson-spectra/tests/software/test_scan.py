import pytest
from tqdm import trange

from spectrum.options import (CompositeNonlinearityScanOptions,
                              NonlinearityScanOptions)
from spectrum.output import open_loggs
from tools.scan import NonlinearityScan
from vault.datavault import DataVault


@pytest.fixture
def nbins():
    return 2


@pytest.fixture
def mc_data(nbins):
    mc = [
        DataVault().input(
            "pythia8",
            listname="PhysNonlinScan",
            histname="MassPt_{}_{}".format(i, j)
        )
        for j in trange(nbins) for i in trange(nbins)
    ]
    return mc


@pytest.fixture
def data():
    return DataVault().input("data", histname="MassPtSM0")


@pytest.fixture
def full_data(data, mc_data):
    return (data, mc_data)


@pytest.mark.onlylocal
@pytest.mark.skip("Don't do nonlinearity scan for pythia8")
def test_interface(full_data):
    estimator = NonlinearityScan(
        NonlinearityScanOptions(nbins=nbins)
    )

    with open_loggs() as loggs:
        assert estimator.transform(full_data, loggs)


@pytest.fixture
def mc_composite_dataset(nbins):
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

    low, high = low.read_multiple(2), high.read_multiple(2)
    mc_data = [(l, h) for l, h in zip(low, high)]
    return mc_data


@pytest.fixture
def full_composite_data(data, mc_composite_dataset):
    return (data, mc_composite_dataset)


@pytest.mark.onlylocal
def test_composite_interface(nbins, full_composite_data):
    estimator = NonlinearityScan(
        CompositeNonlinearityScanOptions(nbins=nbins)
    )

    with open_loggs() as loggs:
        assert estimator.transform(full_composite_data, loggs)
