import unittest
import ROOT

from vault.datavault import DataVault
from vault.formulas import FVault
from spectrum.options import CompositeEfficiencyOptions, Options
from spectrum.efficiency import Efficiency
from spectrum.comparator import Comparator
from spectrum.transformer import TransformerBase
from spectrum.pipeline import Pipeline, ReducePipeline
from spectrum.pipeline import ParallelPipeline, FunctionTransformer
from spectrum.input import SingleHistInput

from spectrum.broot import BROOT as br
from array import array


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


class DebugTheEfficiency(unittest.TestCase):

    def test_efficiency_evaluation(self):
        particle = "#pi^{0}"
        debug_inputs = {
            debug_input("low"): (0, 8),
            debug_input("high"): (4, 20)
        }

        prod = "single #pi^{0} debug8"
        ll = "debug-ledger.json"
        unified_inputs = {
            DataVault(ll).input(prod, "low", listname="PhysEff"): (0, 8.0),
            DataVault(ll).input(prod, "high", listname="PhysEff"): (4.0, 20)
        }

        doptions = CompositeEfficiencyOptions(
            debug_inputs,
            particle,
            genname='hGenPi0Pt_clone',
            use_particle=False,
            ptrange="config/pt-spmc.json",
            scale=0.5
        )
        # doptions.mergeranges = [(0, 6), (6, 20)]

        moptions = CompositeEfficiencyOptions(
            unified_inputs,
            particle,
            genname='hPt_{0}_primary_',
            ptrange="config/pt-spmc.json"
        )

        # moptions.mergeranges = [(0, 6), (6, 20)][::-1]
        CompareEfficiencies(doptions, moptions).transform(
            [debug_inputs, unified_inputs],
            "compare the debug efficiency"
        )
