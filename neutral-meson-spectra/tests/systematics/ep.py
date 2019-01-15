import pytest

from lazy_object_proxy import Proxy
from tools.ep import EpRatioEstimator, DataMCEpRatioEstimator
from tools.mc import Nonlinearity
from spectrum.options import NonlinearityOptions

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


DOUBLE_RATIO_DATASET = Proxy(
    lambda: (
        data("data"),
        data("pythia8", "ep_ratio_1"),
    )
)

VALIDATION_DATA = Proxy(
    lambda:
    (
        DataVault().input("data", histname="MassPtSM0"),
        DataVault().input("pythia8")
    )
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


@pytest.mark.skip("Verifying the production")
@pytest.mark.thesis
@pytest.mark.interactive
@pytest.mark.onlylocal
def test_data_mc_ratio():
    estimator = DataMCEpRatioEstimator(
        DataMCEpRatioOptions(), plot=True
    )
    loggs = AnalysisOutput("test double ep ratio estimator")

    output = estimator.transform(DOUBLE_RATIO_DATASET, loggs=loggs)
    # Comparator(stop=True).compare(output)
    loggs.plot()
    assert len(output) > 0


@pytest.mark.onlylocal
@pytest.mark.interactive
def test_ep_dataset():
    estimator = Nonlinearity(NonlinearityOptions(), plot=True)
    loggs = AnalysisOutput("validate ep ratio")
    output = estimator.transform(VALIDATION_DATA, loggs=loggs)
    # Comparator(stop=True).compare(output)
    # loggs.plot()

    assert len(output) > 0
