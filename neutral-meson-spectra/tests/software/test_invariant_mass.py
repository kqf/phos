import sys
import pytest

from lazy_object_proxy import Proxy
from spectrum.options import Options
from spectrum.processing import DataSlicer, MassFitter, RangeEstimator
from spectrum.processing import InvariantMassExtractor
from spectrum.output import AnalysisOutput
from spectrum.pipeline import Pipeline

from vault.datavault import DataVault


DATASET = Proxy(
    lambda: DataVault().input("data", "stable")
)


@pytest.fixture()
def stop():
    stop = "discover" not in sys.argv
    stop = stop and "pytest" not in sys.argv[0]
    return stop


@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta"
])
def test_draws_multiple(stop, particle):
    option = Options(particle=particle)

    pipeline = Pipeline([
        ("slice", DataSlicer(option.pt)),
        ("extract", InvariantMassExtractor(option.invmass)),
        ("fit", MassFitter(option.invmass.use_mixed)),
        ("ranges", RangeEstimator(option.spectrum)),
    ])

    loggs = AnalysisOutput("test multirage plotter")
    masses = pipeline.transform(DATASET, loggs)
    loggs.update({"invariant-masses": masses})
    loggs.plot(stop=stop)
