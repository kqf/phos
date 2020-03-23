import pytest

from spectrum.options import Options
from spectrum.analysis import Analysis
from spectrum.pipeline import TransformerBase
from spectrum.pipeline import ComparePipeline
from spectrum.output import open_loggs

from spectrum.vault import DataVault


class CompareAnalysis(TransformerBase):
    def __init__(self, steps, particle):
        super(CompareAnalysis, self).__init__()
        options = Options(particle=particle)
        options.output.scalew_spectrum = True
        self.pipeline = ComparePipeline(
            [(step, Analysis(options)) for step in steps],
            plot=True,
        )


@pytest.fixture
def labels():
    return "2017", "total"


@pytest.fixture
def data(labels):
    return (
        DataVault().input("data", "LHC17 qa1"),
        DataVault().input("data", histname="MassPtSM0"),
    )


@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta"
])
def test_gives_similar_results(particle, data, labels):
    assert len(labels) == len(data)

    estimator = CompareAnalysis(
        steps=labels,
        particle=particle
    )
    with open_loggs() as loggs:
        estimator.transform(data, loggs)
