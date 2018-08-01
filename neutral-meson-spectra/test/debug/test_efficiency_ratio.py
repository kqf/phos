import unittest

from spectrum.comparator import Comparator

from spectrum.options import CompositeEfficiencyOptions
from spectrum.output import AnalysisOutput

from vault.datavault import DataVault

from spectrum.transformer import TransformerBase
from spectrum.input import SingleHistInput
from spectrum.analysis import Analysis
from spectrum.pipeline import Pipeline, HistogramSelector
from spectrum.pipeline import ParallelPipeline, HistogramScaler
from spectrum.broot import BROOT as br

# NB: This test is to compare different efficiencies
#     estimated from different productions
#


class SimpleEfficiency(TransformerBase):

    def __init__(self, options, plot=False):
        super(SimpleEfficiency, self).__init__(plot)
        reconstructed = Pipeline([
            ("ReconstructMesons", Analysis(options.analysis)),
            ("NumberOfMesons", HistogramSelector("nmesons")),
            ("ScaleForAcceptance", HistogramScaler(options.scale))
        ])

        self.pipeline = ParallelPipeline([
            ("reconstructed", reconstructed),
            ("generated", SingleHistInput(options.genname)),
        ])


class TestEfficiencyEtaRatio(unittest.TestCase):

    # @unittest.skip('')
    def test_eta_efficiency(self):
        particle = "#eta"
        production = "single #eta updated nonlinearity"
        unified_inputs = {
            DataVault().input(production, "low"): (0.0, 10.0),
            DataVault().input(production, "low"): (0.0, 10.0)
        }
        efficiency = SimpleEfficiency(
            CompositeEfficiencyOptions(unified_inputs, particle).suboptions[0]
        )
        numerator, denominator = efficiency.transform(
            unified_inputs,
            AnalysisOutput("compare numerator with denominator")
        )
        denominator.label = "generated"
        denominator_orig = denominator.Clone()
        denominator_orig.label = "original"
        denominator_orig.logy = True
        numerator, denominator = br.rebin_as(numerator, denominator)
        Comparator().compare(denominator_orig, denominator)
