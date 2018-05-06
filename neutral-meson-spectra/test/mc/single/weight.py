import ROOT
import unittest

from spectrum.options import CompositeCorrectedYieldOptions
from spectrum.corrected_yield import CorrectedYield
# from spectrum.comparator import Comparator
# from spectrum.broot import BROOT as br

from vault.datavault import DataVault
from vault.formulas import FVault


class TestCorrectedYield(unittest.TestCase):

    # @unittest.skip('')
    def test_corrected_yield_for_pi0(self):
        unified_inputs = {
            DataVault().input(
                "single #pi^{0} iteration d2", "low",
                listname="PhysEff1"): (0, 7.0),
            DataVault().input(
                "single #pi^{0} iteration d2", "high",
                listname="PhysEff1"): (7.0, 20)
        }

        data = [
            DataVault().input("data"),
            unified_inputs
        ]

        tsallis = ROOT.TF1("tsallis", FVault().func("tsallis"), 0, 20)

        tsallis.SetParameters(0.014960701090585591,
                              0.287830380417601, 9.921003040859755)
        tsallis.FixParameter(3, 0.135)
        tsallis.FixParameter(4, 0.135)

        options = CompositeCorrectedYieldOptions(
            particle="#pi^{0}",
            unified_inputs=unified_inputs
        )
        options.fitfunc = tsallis
        CorrectedYield(options).transform(data, "corrected yield #pi^{0}")
