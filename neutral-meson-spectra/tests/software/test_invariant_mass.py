import sys
import pytest

from spectrum.options import Options
from spectrum.processing import DataSlicer, MassFitter, RangeEstimator
from spectrum.processing import InvariantMassExtractor
from spectrum.output import open_loggs
from spectrum.pipeline import Pipeline

from vault.datavault import DataVault


@pytest.fixture
def data():
    return DataVault().input("data", histname="MassPtSM0")


@pytest.fixture()
def stop():
    stop = "discover" not in sys.argv
    stop = stop and "pytest" not in sys.argv[0]
    return stop


@pytest.mark.onlylocal
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta"
])
def test_draws_multiple(stop, particle, data):
    option = Options(particle=particle)

    pipeline = Pipeline([
        ("slice", DataSlicer(option.pt)),
        ("extract", InvariantMassExtractor(option.invmass)),
        ("fit", MassFitter(option.invmass.use_mixed)),
        ("ranges", RangeEstimator(option.spectrum)),
    ])

    with open_loggs("multirange plotter", stop=stop) as loggs:
        masses = pipeline.transform(data, loggs)
        loggs.update({"invariant-masses": masses})
