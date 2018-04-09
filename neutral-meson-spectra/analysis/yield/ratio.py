import unittest

from spectrum.corrected_yield import YieldRatio
from spectrum.options import CorrectedYieldOptions

from spectrum.comparator import Comparator
from spectrum.broot import BROOT as br
from vault.datavault import DataVault


class TestNeutralMesonYieldRatio(unittest.TestCase):


    def test_yield_ratios(self):
        # Define the inputs and the dataset for #eta mesons
        #
        unified_inputs_eta = {
            DataVault().input("single #eta updated", "low"):  (0, 6.0),
            DataVault().input("single #eta updated", "high"): (6.0, 20)
        }

        data_eta = [
            DataVault().input("data"),
            unified_inputs_eta
        ]

        options_eta = CorrectedYieldOptions(
            particle="#eta",
            unified_inputs=unified_inputs_eta
        )


        # Define the inputs and the dataset for #pi^{0}
        #
        unified_inputs_pi0 = {
            DataVault().input("single #pi^{0} corrected weights", "low"):  (0, 7.0),
            DataVault().input("single #pi^{0} corrected weights", "high"): (7.0, 20)
        }

        data_pi0 = [
            DataVault().input("data"),
            unified_inputs_pi0
        ]


        options_pi0 = CorrectedYieldOptions(
            particle="#pi^{0}",
            unified_inputs=unified_inputs_pi0
        )


        # Make same binning for all neutral mesons
        options_pi0.set_binning(
            options_eta.analysis.pt.ptedges,
            options_eta.analysis.pt.rebins
        )

        estimator = YieldRatio(
            options_eta=options_eta,
            options_pi0=options_pi0
        )


        estimator.transform(
            [data_eta, data_pi0],
            "eta to pion ratio"
        )
