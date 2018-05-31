import unittest

from spectrum.corrected_yield import YieldRatio, CorrectedYield
from spectrum.options import CompositeCorrectedYieldOptions
from spectrum.output import AnalysisOutput
from spectrum.comparator import Comparator
import spectrum.sutils as su

from vault.datavault import DataVault


def ratio_input():
    # Define the inputs and the dataset for #eta mesons
    #
    unified_inputs_eta = {
        DataVault().input("single #eta updated", "low"): (0, 6.0),
        DataVault().input("single #eta updated", "high"): (6.0, 20)
    }

    data_eta = [
        DataVault().input("data"),
        unified_inputs_eta
    ]

    options_eta = CompositeCorrectedYieldOptions(
        particle="#eta",
        unified_inputs=unified_inputs_eta
    )

    # Define the inputs and the dataset for #pi^{0}
    #
    prod = "single #pi^{0} iteration3 yield aliphysics"
    unified_inputs_pi0 = {
        DataVault().input(prod, "low"): (0, 7.0),
        DataVault().input(prod, "high"): (7.0, 20)
    }

    data_pi0 = [
        DataVault().input("data"),
        unified_inputs_pi0
    ]

    options_pi0 = CompositeCorrectedYieldOptions(
        particle="#pi^{0}",
        unified_inputs=unified_inputs_pi0
    )
    # Make same binning for all neutral mesons
    options_pi0.set_binning(
        options_eta.analysis.pt.ptedges,
        options_eta.analysis.pt.rebins
    )
    return data_eta, options_eta, data_pi0, options_pi0


class TestNeutralMesonYieldRatio(unittest.TestCase):

    def test_yield_ratio(self):
        data_eta, options_eta, data_pi0, options_pi0 = ratio_input()

        estimator = YieldRatio(
            options_eta=options_eta,
            options_pi0=options_pi0,
            plot=True
        )

        output = estimator.transform(
            [data_eta, data_pi0],
            loggs=AnalysisOutput("eta to pion ratio")
        )
        Comparator().compare(output)

    @unittest.skip('Something is wrong')
    def test_debug_ratio(self):
        data_eta, options_eta, data_pi0, options_pi0 = ratio_input()
        loggs = AnalysisOutput("")
        pi0 = CorrectedYield(options_pi0).transform(data_pi0, loggs)
        eta = CorrectedYield(options_eta).transform(data_eta, loggs)

        su.wait()
        Comparator().compare(eta, pi0)
