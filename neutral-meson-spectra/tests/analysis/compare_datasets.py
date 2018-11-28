import pytest

from spectrum.options import Options
from spectrum.analysis import Analysis
from spectrum.pipeline import TransformerBase
from spectrum.pipeline import ComparePipeline
from spectrum.output import AnalysisOutput

from vault.datavault import DataVault


class CompareAnalysis(TransformerBase):
    def __init__(self, steps, particle):
        super(CompareAnalysis, self).__init__()
        options = Options(particle=particle)
        options.output.scalew_spectrum = True
        self.pipeline = ComparePipeline(
            [(step, Analysis(options)) for step in steps],
            plot=True,
        )


@pytest.mark.interactive
@pytest.mark.onlylocal
@pytest.mark.parametrize("particle", ["#pi^{0}", "#eta"])
def test_gives_similar_results(particle):
    data = (
        DataVault().input("data", "ep_ratio", label="2016 new aliphysics"),
        DataVault().input("data", "LHC17 qa1", label="2017"),
        DataVault().input("data", label="2016"),
    )

    estimator = CompareAnalysis(
        steps=[d.label for d in data],
        particle=particle
    )

    loggs = AnalysisOutput("compare different datasets", particle=particle)
    estimator.transform(data, loggs)
    loggs.plot()
