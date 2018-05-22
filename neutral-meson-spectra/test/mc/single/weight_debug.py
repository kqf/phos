import ROOT
import unittest

from spectrum.pipeline import Pipeline
from spectrum.pipeline import OutputFitter
from spectrum.input import SingleHistInput
from spectrum.options import Options
from spectrum.output import AnalysisOutput
# from spectrum.comparator import Comparator
# from spectrum.broot import BROOT as br

from vault.datavault import DataVault
from vault.formulas import FVault


class TestCorrectedYield(unittest.TestCase):

    # @unittest.skip('')
    def test_corrected_yield_for_pi0(self):
        mcdata = DataVault().input(
            "single #pi^{0} iteration d3 nonlin9", "low",
            listname="PhysEff1")

        tsallis = ROOT.TF1(
            "tsallis",
            FVault().func("tsallis", "standard"), 0, 10)
        parameters = [0.2622666606436988,
                      0.08435275173194286,
                      7.356520553419461]
        for i, par in enumerate(parameters):
            tsallis.FixParameter(i, par)

        # tsallis.SetParameters(0.014960701090585591,
        # 0.287830380417601, 9.921003040859755)
        tsallis.FixParameter(3, 0.135)
        tsallis.FixParameter(4, 0.135)

        options = Options()
        options.fitfunc = tsallis
        estimator = Pipeline([
            ("data", SingleHistInput(
                "hPt_#pi^{0}_primary_standard", norm=True)),
            ("fit", OutputFitter(options)),
        ])

        estimator.transform(mcdata, AnalysisOutput("corrected yield #pi^{0}"))
