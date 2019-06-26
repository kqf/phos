import pytest
from spectrum.comparator import Comparator
from spectrum.options import (DataMCEpRatioOptions, EpRatioOptions,
                              NonlinearityOptions)
from spectrum.output import AnalysisOutput
from tools.ep import DataMCEpRatioEstimator, EpRatioEstimator
from tools.mc import Nonlinearity
from vault.datavault import DataVault


# from spectrum.output import AnalysisOutput


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
        data_old_selection("data", "nonlinearity"),
        data_old_selection("pythia8", "nonlinearity"),
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
    output = estimator.transform(
        data("pythia8", "ep_ratio_1"),
        loggs="test ep ratio estimator"
    )

    for o in output:
        Comparator().compare(o)


@pytest.mark.skip("")
def test_ep_ratio_data():
    options = EpRatioOptions()
    estimator = EpRatioEstimator(options, plot=True)
    output = estimator.transform(
        data("data"),
        loggs="test ep ratio estimator"
    )

    for o in output:
        Comparator().compare(o)


@pytest.mark.thesis
@pytest.mark.interactive
@pytest.mark.onlylocal
def test_data_mc_ratio(double_ratio_data):
    estimator = DataMCEpRatioEstimator(
        DataMCEpRatioOptions(), plot=True
    )
    loggs = AnalysisOutput("double ep ratio")

    output = estimator.transform(double_ratio_data, loggs=loggs)
    # Comparator(stop=True).compare(output)
    loggs.plot()
    assert len(output) > 0


@pytest.mark.skip("Verifying the production")
@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta",
])
def test_ep_dataset(particle, validation_data):
    estimator = Nonlinearity(
        NonlinearityOptions(particle=particle), plot=True
    )
    loggs = AnalysisOutput("validate ep ratio")
    output = estimator.transform(validation_data, loggs=loggs)
    # Comparator(stop=True).compare(output)
    # loggs.plot()
    assert len(output) > 0
