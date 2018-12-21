import unittest
import ROOT

from spectrum.input import Input, SingleHistInput
from spectrum.output import AnalysisOutput
from spectrum.comparator import Comparator
from spectrum.pipeline import ComparePipeline, Pipeline, HistogramSelector
from spectrum.analysis import Analysis

from spectrum.options import Options

from vault.datavault import DataVault
from vault.formulas import FVault


class FunctionOutput(object):

    def __init__(self, func):
        super(FunctionOutput, self).__init__()
        self.func = func

    def transform(self, inputs, loggs):
        return self.func


class ReconstructedValidator(object):
    def __init__(self, func, options=Options()):
        super(ReconstructedValidator, self).__init__()
        nmesons = Pipeline([
            ("ReconstructMesons", Analysis(options)),
            ("NumberOfMesons", HistogramSelector("nmesons"))
        ])
        self.runion = ComparePipeline([
            ("nmesons", nmesons),
            ("func", FunctionOutput(func))
        ])


def tsallis():
    tsallis = ROOT.TF1("f", FVault().func("tsallis"), 0, 100)
    tsallis.SetParameters(0.014960701090585591,
                          0.287830380417601, 9.921003040859755)
    # [0.014850211992453644, 0.28695967166609104, 9.90060126848571
    tsallis.FixParameter(3, 0.135)
    tsallis.FixParameter(4, 0.135)
    tsallis.label = "tsallis"
    return tsallis


class ValidateReconstructedPi0(unittest.TestCase):

    def test_pi0_generated(self):
        estimator = ReconstructedValidator(
            tsallis(),
            Options.spmc((8.0, 20.0), particle="#pi^{0}")
        )

        loggs = AnalysisOutput(
            "test_spectrum_extraction_spmc_{}".format("#pi^{0}"), "#pi^{0}")
        output = estimator.transform(
            (
                Input(DataVault().file("single #pi^{0}", "high"), "PhysEff"),
                None
            ),
            loggs
        )
        loggs.plot(False)

        output.logy = False
        diff = Comparator(stop=True, crange=(0, 8000))
        diff.compare(output)


class GeneratedValidator(object):
    def __init__(self, func, histname):
        super(GeneratedValidator, self).__init__()
        self.runion = ComparePipeline([
            ("hist", SingleHistInput(histname)),
            ("func", FunctionOutput(func))
        ])


MC_INPUT = (
    DataVault().input("single #pi^{0}", "high", listname="PhysEff"),
    None
)


def test_pi0_generated():
    estimator = GeneratedValidator(tsallis(), "hPt_#pi^{0}_primary_standard")

    loggs = AnalysisOutput(
        "generated_spectrum_extraction_spmc_{}".format("#pi^{0}"))
    output = estimator.transform(MC_INPUT, loggs)
    loggs.plot(False)

    output.logy = False
    diff = Comparator(stop=True)
    diff.compare(output)
