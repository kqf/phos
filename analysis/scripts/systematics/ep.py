import pytest
import spectrum.broot as br
from spectrum.comparator import Comparator
from spectrum.options import DataMCEpRatioOptions, EpRatioOptions
from spectrum.output import open_loggs
from spectrum.tools.ep import DataMCEpRatioEstimator, EpRatioEstimator
from spectrum.vault import DataVault
from spectrum.tools.validate import validate


def data_old_selection(prod="data", version="ep_ratio"):
    return DataVault().input(
        prod,
        version=version,
        listname="EpRatio",
        histname="EpElectronsPSM0",
        suffixes=None)


def data(prod="data", version="ep_ratio"):
    return DataVault().input(
        prod,
        version=version,
        listname="PHOSEpRatioCoutput1",
        histname="Ep_ele",
        suffixes=None)


@pytest.fixture
def double_ratio_data():
    return (
        data_old_selection("data", "tof"),
        data_old_selection("pythia8", "latest"),
    )


@pytest.fixture
def validation_data():
    return (
        DataVault().input("data", histname="MassPtSM0"),
        DataVault().input("pythia8")
    )


@pytest.mark.skip
def test_ep_ratio_mc():
    options = EpRatioOptions()
    estimator = EpRatioEstimator(options, plot=True)

    with open_loggs() as loggs:
        output = estimator.transform(data("pythia8", "latest"), loggs)
    Comparator().compare(output)


@pytest.mark.skip
def test_ep_ratio_data():
    options = EpRatioOptions()
    estimator = EpRatioEstimator(options, plot=True)

    with open_loggs() as loggs:
        output = estimator.transform(data("data", "latest"), loggs)
    Comparator().compare(output)


# Benchmark:
# In the 5 TeV analysis E/p(data) / E/p (MC) ~ 0.004

@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.interactive
def test_data_mc_ratio(double_ratio_data, stop):
    estimator = DataMCEpRatioEstimator(
        DataMCEpRatioOptions(), plot=stop
    )
    with open_loggs() as loggs:
        output = estimator.transform(double_ratio_data, loggs)
        Comparator(stop=stop).compare(output)
    validate(br.hist2dict(output), "double_ep_ratio")
