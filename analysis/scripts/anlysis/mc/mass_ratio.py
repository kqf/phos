import pytest

from spectrum.analysis import Analysis
from spectrum.pipeline import TransformerBase
from spectrum.pipeline import Pipeline
from spectrum.pipeline import ComparePipeline
from spectrum.pipeline import HistogramSelector
from spectrum.options import CompositeOptions
from spectrum.output import open_loggs
from spectrum.vault import DataVault


class MassComparator(TransformerBase):
    def __init__(self, options_eta, options_pion, plot=False):
        super(MassComparator, self).__init__(plot)
        self.pipeline = ComparePipeline([
            ("#pi^{0}", Pipeline([
                ("analysis", Analysis(options_eta, plot)),
                ("spectrum", HistogramSelector("mass"))
            ])),
            ("#eta", Pipeline([
                ("analysis", Analysis(options_pion, plot)),
                ("spectrum", HistogramSelector("mass"))
            ])),
        ], plot=plot)


@pytest.fixture
def pion_data():
    return (
        DataVault().input("single #pi^{0}", "low", "PhysEff"),
        DataVault().input("single #pi^{0}", "high", "PhysEff")
    )


@pytest.fixture
def eta_data():
    return (
        DataVault().input("single #eta", "low", "PhysEff"),
        DataVault().input("single #eta", "high", "PhysEff")
    )


@pytest.fixture
def data(pion_data, eta_data):
    return pion_data, eta_data


@pytest.mark.onlylocal
def test_efficiency_ratio(data, pt="config/pt-same.json"):
    estimator = MassComparator(
        CompositeOptions("#pi^{0}", pt=pt),
        CompositeOptions("#eta", pt=pt),
        plot=True
    )
    with open_loggs() as loggs:
        estimator.transform(data, loggs)
