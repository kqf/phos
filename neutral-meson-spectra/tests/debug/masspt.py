import pytest

from vault.datavault import DataVault
from spectrum.efficiency import Efficiency
from spectrum.comparator import Comparator
from spectrum.pipeline import TransformerBase
from spectrum.pipeline import ReducePipeline
from spectrum.pipeline import ParallelPipeline
from spectrum.options import CompositeEfficiencyOptions


class CompareEfficiencies(TransformerBase):
    def __init__(self, options1, options2, plot=False):
        super(CompareEfficiencies, self).__init__(plot)
        self.pipeline = ReducePipeline(
            ParallelPipeline([
                ("debug", Efficiency(options1)),
                ("real", Efficiency(options2))
            ]),
            Comparator().compare
        )


def debug_input(prod="low"):
    return DataVault().input(
        "debug efficiency",
        prod,
        n_events=1,
        histnames=('hSparseMgg_proj_0_1_3_yx', ''),
        label=prod)


@pytest.fixture
def data():
    debug_set = (
        debug_input("low"),
        debug_input("high"),
    )
    prod_set = (
        DataVault().input("single #pi^{0}", "low", listname="PhysEff"),
        DataVault().input("single #pi^{0}", "high", listname="PhysEff"),
    )
    return debug_set, prod_set


@pytest.mark.onlylocal
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    # "#eta",
])
def test_efficiency_evaluation(particle, data):
    doptions = CompositeEfficiencyOptions(
        particle,
        genname='hGenPi0Pt_clone',
        use_particle=False,
        pt="config/pt.json",
        scale=0.5
    )

    moptions = CompositeEfficiencyOptions(
        particle,
        genname='hPt_{0}_primary_',
        pt="config/pt.json"
    )

    CompareEfficiencies(doptions, moptions).transform(
        data,
        "compare the debug efficiency"
    )
