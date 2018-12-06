import pytest

from tools.ep import EpRatioEstimator, DataMCEpRatioEstimator

from vault.datavault import DataVault
from spectrum.options import EpRatioOptions, DataMCEpRatioOptions
from spectrum.comparator import Comparator
from spectrum.output import AnalysisOutput
# from spectrum.output import AnalysisOutput


def data(prod="data", version="ep_ratio"):
    return DataVault().input(
        prod,
        version=version,
        listname="PHOSEpRatioCoutput1",
        histname="Ep_ele",
        use_mixing=False)


DOUBLE_RATIO_DATASET = (
    data("data"),
    data("pythia8", "ep_ratio_1"),
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


def test_data_mc_ratio():
    estimator = DataMCEpRatioEstimator(
        DataMCEpRatioOptions(), plot=True
    )
    loggs = AnalysisOutput("test double ep ratio estimator")

    output = estimator.transform(DOUBLE_RATIO_DATASET, loggs=loggs)
    # Comparator(stop=True).compare(output)
    loggs.plot()
    assert len(output) > 0
