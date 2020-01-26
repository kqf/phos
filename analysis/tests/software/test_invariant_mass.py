import pytest

from spectrum.options import Options
from spectrum.output import open_loggs
from spectrum.pipeline import Pipeline
from spectrum.processing import (DataPreparator, InvariantMassExtractor,
                                 MassFitter, RangeEstimator)

from spectrum.vault import DataVault


@pytest.fixture
def data():
    return DataVault().input("data", histname="MassPtSM0")


@pytest.mark.onlylocal
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta"
])
def test_draws_multiple(stop, particle, data):
    option = Options(particle=particle)

    pipeline = Pipeline([
        ("slice", DataPreparator(option.pt)),
        ("extract", InvariantMassExtractor(option.invmass)),
        ("fit", MassFitter(option.invmass.use_mixed)),
        ("ranges", RangeEstimator(option.calibration)),
    ])

    with open_loggs("multirange plotter", stop=stop) as loggs:
        masses = pipeline.transform(data, loggs)
        loggs.update({"invariant-masses": masses})
