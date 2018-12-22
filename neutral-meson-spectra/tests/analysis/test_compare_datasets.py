import pytest

from lazy_object_proxy import Proxy
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


DATASETS = Proxy(
    lambda: (
        DataVault().input("data", "ep_ratio", histname="MassPtSM0",
                          label="2016 new aliphysics"),
        DataVault().input("data", "LHC17 qa1", label="2017"),
        DataVault().input("data", label="2016", histname="MassPtSM0"),
    )
)


@pytest.mark.interactive
@pytest.mark.onlylocal
@pytest.mark.parametrize("particle", ["#pi^{0}", "#eta"])
def test_gives_similar_results(particle):
    estimator = CompareAnalysis(
        steps=[d.label for d in DATASETS],
        particle=particle
    )

    loggs = AnalysisOutput("compare different datasets", particle=particle)
    estimator.transform(DATASETS, loggs)
    loggs.plot()
