import pytest  # noqa

from lazy_object_proxy import Proxy
from spectrum.analysis import Analysis
from spectrum.pipeline import TransformerBase
from spectrum.pipeline import Pipeline
from spectrum.pipeline import ComparePipeline
from spectrum.pipeline import HistogramSelector
from spectrum.options import CompositeOptions
from spectrum.output import AnalysisOutput
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


PION_DATA = Proxy(
    lambda:
    (
        DataVault().input("single #pi^{0}", "low", "PhysEff", label="#pi^{0}"),
        DataVault().input("single #pi^{0}", "high", "PhysEff", label="#pi^{0}")
    )
)
ETA_DATA = Proxy(
    lambda:
    (
        DataVault().input("single #eta", "low", "PhysEff", label="#eta"),
        DataVault().input("single #eta", "high", "PhysEff", label="#eta")
    )
)


@pytest.mark.onlylocal
def test_efficiency_ratio():
    ptrange = "config/pt-same.json"
    opt_eta = CompositeOptions("#eta", ptrange=ptrange)
    opt_pi0 = CompositeOptions("#pi^{0}", ptrange=ptrange)
    estimator = MassComparator(opt_eta, opt_pi0, plot=False)
    loggs = AnalysisOutput("mass ratio")
    estimator.transform((ETA_DATA, PION_DATA), loggs)
    # loggs.plot()
