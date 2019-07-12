import pytest

from spectrum.analysis import Analysis
from spectrum.pipeline import TransformerBase
from spectrum.pipeline import Pipeline
from spectrum.pipeline import ComparePipeline
from spectrum.pipeline import HistogramSelector
from spectrum.options import CompositeOptions
from spectrum.output import open_loggs
from vault.datavault import DataVault


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
        ])


@pytest.fixture
def pion_data():
    return (
        DataVault().input("single #pi^{0}", "low", "PhysEff", label="#pi^{0}"),
        DataVault().input("single #pi^{0}", "high", "PhysEff", label="#pi^{0}")
    )


@pytest.fixture
def eta_data():
    return (
        DataVault().input("single #eta", "low", "PhysEff", label="#eta"),
        DataVault().input("single #eta", "high", "PhysEff", label="#eta")
    )


@pytest.fixture
def data(pion_data, eta_data):
    return eta_data, pion_data


@pytest.mark.onlylocal
def test_efficiency_ratio(data):
    pt = "config/pt-same.json"
    opt_eta = CompositeOptions("#eta", pt=pt)
    opt_pi0 = CompositeOptions("#pi^{0}", pt=pt)
    estimator = MassComparator(opt_eta, opt_pi0, plot=False)

    with open_loggs("mass ratio") as loggs:
        estimator.transform(data, loggs)
