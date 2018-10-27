import unittest

from spectrum.pipeline import TransformerBase
from spectrum.options import CompositeEfficiencyOptions
from spectrum.pipeline import Pipeline, ComparePipeline
from spectrum.processing import DataSlicer, MassFitter
from spectrum.output import AnalysisOutput
from vault.datavault import DataVault
# NB: This test is to compare different efficiencies
#     estimated from different productions
#


class SignalExtractor(TransformerBase):
    def transform(self, data, loggs):
        signals = [m.mass for m in data
                   if m.pt_range[0] >= 4 and m.pt_range[1] <= 8]
        for s, m in zip(signals, data):
            s.SetAxisRange(0.08, 0.2, "X")
            s.GetListOfFunctions().Clear()
            s.label = m.pt_label
        return signals


class SignalScaler(TransformerBase):
    def __init__(self, options):
        low_pt = options.spectrum.ptrange[-1] < 19
        self.scale = 0.02 if low_pt else 1.0

    def transform(self, data, loggs):
        for h in data:
            h.Scale(self.scale)
        return data


class SimpleAnalysis(TransformerBase):

    def __init__(self, options, plot=False):
        super(SimpleAnalysis, self).__init__(plot)
        self.options = options
        self.pipeline = Pipeline([
            ("slice", DataSlicer(options.pt)),
            ("fitmasses", MassFitter(options.invmass)),
            ("signals", SignalExtractor()),
            ("scale", SignalScaler(options))
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
        production = "single #pi^{0} debug3"
        options = CompositeEfficiencyOptions(
            particle,
            ptrange="config/pt-debug.json"
        )
        loggs = AnalysisOutput("mass_test_{}".format(particle))
        MassComparator(options, plot=True).transform(
            (
                DataVault().input(production, "low", "PhysEff"),
                DataVault().input(production, "high", "PhysEff"),
            ),
            loggs
        )
        # diff.compare(efficiency)
        loggs.plot()
