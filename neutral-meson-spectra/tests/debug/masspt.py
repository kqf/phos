import pytest

from lazy_object_proxy import Proxy
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
        inputs=('hSparseMgg_proj_0_1_3_yx', ''),
        label=prod)


DATASETS = Proxy(
    lambda:
    (
        debug_input("low"),
        debug_input("high"),
    ),
    (
        DataVault().input("single #pi^{0}", "low", listname="PhysEff"),
        DataVault().input("single #pi^{0}", "high", listname="PhysEff"),
    )
)


@pytest.mark.onlylocal
def test_efficiency_evaluation(self):
    particle = "#pi^{0}"
    doptions = CompositeEfficiencyOptions(
        particle,
        genname='hGenPi0Pt_clone',
        use_particle=False,
        ptrange="config/pt-spmc.json",
        scale=0.5
    )

    moptions = CompositeEfficiencyOptions(
        particle,
        genname='hPt_{0}_primary_',
        ptrange="config/pt-spmc.json"
    )

    CompareEfficiencies(doptions, moptions).transform(
        DATASETS,
        "compare the debug efficiency"
    )
