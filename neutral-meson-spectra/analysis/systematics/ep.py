import pytest
from spectrum.comparator import Comparator
from spectrum.options import DataMCEpRatioOptions, EpRatioOptions
from spectrum.output import open_loggs
from tools.ep import DataMCEpRatioEstimator, EpRatioEstimator
from vault.datavault import DataVault


def data_old_selection(prod="data", version="ep_ratio"):
    return DataVault().input(
        prod,
        version=version,
        listname="EpRatio",
        histname="EpElectronsPSM0",
        use_mixing=False)


def data(prod="data", version="ep_ratio"):
    return DataVault().input(
        prod,
        version=version,
        listname="PHOSEpRatioCoutput1",
        histname="Ep_ele",
        use_mixing=False)


@pytest.fixture
def double_ratio_data():
    return (
        data_old_selection("data", "latest"),
        data_old_selection("pythia8", "latest"),
    )


@pytest.fixture
def validation_data():
    return (
        DataVault().input("data", histname="MassPtSM0"),
        DataVault().input("pythia8")
    )


@pytest.mark.skip("")
def test_ep_ratio_mc():
    options = EpRatioOptions()
    estimator = EpRatioEstimator(options, plot=True)

    with open_loggs() as loggs:
        output = estimator.transform(data("pythia8", "latest"), loggs)
    Comparator().compare(output)


@pytest.mark.skip("")
def test_ep_ratio_data():
    options = EpRatioOptions()
    estimator = EpRatioEstimator(options, plot=True)

    with open_loggs() as loggs:
        output = estimator.transform(data("data", "latest"), loggs)
    Comparator().compare(output)


@pytest.mark.thesis
@pytest.mark.interactive
@pytest.mark.onlylocal
def test_data_mc_ratio(double_ratio_data):
    estimator = DataMCEpRatioEstimator(
        DataMCEpRatioOptions(), plot=True
    )
    with open_loggs("double ep ratio") as loggs:
        output = estimator.transform(double_ratio_data, loggs)
        Comparator().compare(output)
    assert len(output) > 0
