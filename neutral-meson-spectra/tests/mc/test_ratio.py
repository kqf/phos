import pytest

from lazy_object_proxy import Proxy
from spectrum.analysis import Analysis
from spectrum.pipeline import Pipeline, ComparePipeline, HistogramSelector
from spectrum.options import Options
from spectrum.output import AnalysisOutput

from vault.datavault import DataVault

ETA_INPUTS = Proxy(
    lambda x: DataVault().input("single #eta", "high", "PhysEff")
)

PI0_INPUTS = Proxy(
    lambda x: DataVault().input("single #pi^{0}", "low", "PhysEff")
)


@pytest.mark.onlylocal
def test_compare_raw_yields():
    ptrange = "config/pt-same.json"
    estimator = ComparePipeline([
        ("#eta", Pipeline([
            "analysis", Analysis(Options(particle="#pi^{0}", ptrange=ptrange)),
            "spectrum", HistogramSelector("spectrum")
        ])),
        ("#pi^{0}", Pipeline([
            "analysis", Analysis(Options(particle="#eta", ptrange=ptrange)),
            "spectrum", HistogramSelector("spectrum")
        ])),
    ])
    loggs = AnalysisOutput("efficiency_ratio")
    estimator.transform((ETA_INPUTS, PI0_INPUTS), loggs)
    loggs.plot()
