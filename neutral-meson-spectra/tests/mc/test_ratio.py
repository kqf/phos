import pytest

from spectrum.analysis import Analysis
from spectrum.pipeline import Pipeline, ComparePipeline, HistogramSelector
from spectrum.options import Options
from spectrum.output import AnalysisOutput

from vault.datavault import DataVault


@pytest.fixture
def dataset():
    return (
        DataVault().input("pythia8", "high", "PhysEff"),
        DataVault().input("pythia8", "low", "PhysEff")
    )


@pytest.mark.onlylocal
def test_compare_raw_yields(dataset):
    ptrange = "config/pt-same.json"
    estimator = ComparePipeline([
        ("#pi^{0}", Pipeline([
            "analysis", Analysis(Options(particle="#eta", ptrange=ptrange)),
            "spectrum", HistogramSelector("spectrum")
        ])),
        ("#eta", Pipeline([
            "analysis", Analysis(Options(particle="#pi^{0}", ptrange=ptrange)),
            "spectrum", HistogramSelector("spectrum")
        ])),
    ])
    loggs = AnalysisOutput("efficiency_ratio")
    estimator.transform(dataset, loggs)
    loggs.plot()
