import unittest
import ROOT

from spectrum.input import Input, SingleHistInput
from spectrum.output import AnalysisOutput
from spectrum.comparator import Comparator
from spectrum.pipeline import RatioUnion, Pipeline, HistogramSelector
from spectrum.analysis import Analysis

from spectrum.options import Options

from vault.datavault import DataVault


class FunctionOutput(object):

    def __init__(self, func):
        super(FunctionOutput, self).__init__()
        self.func = func

    def transform(self, inputs, loggs):
        return self.func


class ReconstructedValidator(object):
    def __init__(self, func, options=Options()):
        super(ReconstructedValidator, self).__init__()
        self.runion = RatioUnion(
            Pipeline([
                ("ReconstructMesons", Analysis(options)),
                ("NumberOfMesons", HistogramSelector("nmesons"))
            ]),
            FunctionOutput(func)
        )

    def transform(self, inputs, loggs):
        ratio = self.runion.transform(inputs, loggs)
        return ratio


def tsallis():
    tsallis = ROOT.TF1(
        "f", "x[0] * (x[0] )*[0]/2./3.1415*([2]-1.)*([2]-2.)/([2]*[1]*([2]*[1]+[4]*([2]-2.))) * (1.+(sqrt((x[0])*(x[0])+[3]*[3])-[4])/([2]*[1])) ** (-[2])", 0, 100)
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
            Options.spmc((7, 20), particle="#pi^{0}")
        )

        loggs = AnalysisOutput(
            "test_spectrum_extraction_spmc_{}".format("#pi^{0}"), "#pi^{0}")
        output = estimator.transform(
            Input(DataVault().file("single #pi^{0}", "high"), "PhysEff"),
            loggs
        )
        loggs.plot(False)

        output.logy = False
        diff = Comparator(stop=True, crange=(0, 8000))
        diff.compare(output)


class GeneratedValidator(object):
    def __init__(self, func, histname):
        super(GeneratedValidator, self).__init__()
        self.runion = RatioUnion(
            SingleHistInput(histname),
            FunctionOutput(func)
        )

    def transform(self, inputs, loggs):
        ratio = self.runion.transform(inputs, loggs)
        return ratio


class ValidateGeneratedPi0(unittest.TestCase):

    def test_pi0_generated(self):
        estimator = GeneratedValidator(
            tsallis(),
            "hPt_#pi^{0}_primary_standard"
        )

        loggs = AnalysisOutput(
            "generated_spectrum_extraction_spmc_{}".format("#pi^{0}"), "#pi^{0}")
        output = estimator.transform(
            Input(DataVault().file("single #pi^{0}", "high"), "PhysEff"),
            loggs
        )
        loggs.plot(False)

        output.logy = False
        diff = Comparator(stop=True)
        diff.compare(output)
