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
        prod = "single #pi^{0}"
        inputs = (
            DataVault().input(prod, "low", listname="PhysEff"),
            DataVault().input(prod, "high", listname="PhysEff"),
        )

        tsallis = ROOT.TF1("tsallis", FVault().func("tsallis"), 0, 10)
        tsallis.SetParameters(0.014960701090585591,
                              0.287830380417601, 9.921003040859755)
        tsallis.FixParameter(3, 0.135)
        tsallis.FixParameter(4, 0.135)

        options = CompositeCorrectedYieldOptions(particle="#pi^{0}")
        options.fitfunc = tsallis
        CorrectedYield(options).transform(
            (
                DataVault().input("data"),
                inputs
            ),
            "corrected yield #pi^{0}"
        )
