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
def data():
    return (
        DataVault().input("data", "LHC17 qa1", label="2017"),
        DataVault().input("data", label="2016", histname="MassPtSM0"),
    )


@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle", ["#pi^{0}", "#eta"])
def test_gives_similar_results(particle, data):
    estimator = CompareAnalysis(
        steps=[d.label for d in data],
        particle=particle
    )

    with open_loggs("compare different datasets") as loggs:
        estimator.transform(data, loggs)
