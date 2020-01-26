import pytest

from spectrum.pipeline import TransformerBase
from spectrum.options import CompositeEfficiencyOptions
from spectrum.pipeline import Pipeline, ComparePipeline
from spectrum.processing import DataPreparator, MassFitter
from spectrum.output import open_loggs
from spectrum.vault import DataVault
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
        low_pt = options.calibration.ptrange[-1] < 19
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
            ("slice", DataPreparator(options.pt)),
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
        return "{0} < p_{T} < {1} GeV/#it{c}".format(*ranges, T='{T}')


@pytest.fixture
def data():
    return (
        DataVault().input("single #pi^{0}", "low", "PhysEff"),
        DataVault().input("single #pi^{0}", "high", "PhysEff"),
    )


@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta",
])
def test_efficiency(particle, data):
    options = CompositeEfficiencyOptions(
        particle,
        pt="config/pt-debug.json"
    )

    with open_loggs("mass_test_{}".format(particle)) as loggs:
        MassComparator(options, plot=True).transform(data, loggs)
