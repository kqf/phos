import unittest

from spectrum.transformer import TransformerBase
from spectrum.options import CompositeEfficiencyOptions
from spectrum.pipeline import Pipeline, ComparePipeline
from spectrum.processing import DataSlicer, MassFitter
from spectrum.output import AnalysisOutput
from vault.datavault import DataVault
from spectrum.broot import BROOT as br
# NB: This test is to compare different efficiencies
#     estimated from different productions
#


class SignalExtractor(TransformerBase):
    def transform(self, data, loggs):
        signals = [m.mass for m in data
                   if m.pt_range[0] > 4 and m.pt_range[1] < 8]
        for s in signals:
            s.SetAxisRange(0.08, 0.2, "X")
        return signals


class SimpleAnalysis(TransformerBase):

    def __init__(self, options, plot=False):
        super(SimpleAnalysis, self).__init__(plot)
        self.options = options
        self.pipeline = Pipeline([
            ("slice", DataSlicer(options.pt)),
            ("fitmasses", MassFitter(options.invmass)),
            ("signals", SignalExtractor()),
        ])


class MassComparator(TransformerBase):

    def __init__(self, options, plot=False):
        super(MassComparator, self).__init__(plot)
        self.pipeline = ComparePipeline([
            (self._stepname(ranges), SimpleAnalysis(opt.analysis, plot))
            for (opt, ranges) in zip(options.suboptions,
                                     options.mergeranges)
        ], rrange=(0, 4))

    def _stepname(self, ranges):
        return "{0} < p_{T} < {1} GeV/c".format(*ranges, T='{T}')


class TestMasses(unittest.TestCase):

    # @unittest.skip('')
    def test_efficiency(self):
        # production = "single #pi^{0} iteration3 yield aliphysics"
        particle = "#pi^{0}"
        production = "single #pi^{0} iteration d3 nonlin14"
        unified_inputs = {
            DataVault().input(production, "low", "PhysEff"): (0.0, 8.0),
            # DataVault().input(production, "high", "PhysEff"): (4.0, 20.0),
            DataVault().input(production, "high", "PhysEff"): (4.0, 20.0),
        }
        options = CompositeEfficiencyOptions(unified_inputs, particle)
        loggs = AnalysisOutput("mass_test_{}".format(particle))
        MassComparator(options, plot=True).transform(
            unified_inputs,
            loggs
        )
        # diff.compare(efficiency)
        loggs.plot()
