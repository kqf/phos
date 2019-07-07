from __future__ import print_function
import ROOT
import pytest

from spectrum.pipeline import TransformerBase
from spectrum.options import CompositeEfficiencyOptions, OptionsSPMC
from spectrum.pipeline import Pipeline, ComparePipeline
from spectrum.processing import DataSlicer, MassFitter
from spectrum.processing import InvariantMassExtractor
from spectrum.output import open_loggs
from vault.datavault import DataVault
from spectrum.comparator import Comparator
from spectrum.broot import BROOT as br
# NB: This test is to compare different efficiencies
#     estimated from different productions
#


class SignalCutOff(TransformerBase):
    def __init__(self, mrange, plot=False):
        super(SignalCutOff, self).__init__(plot)
        self.mrange = mrange

    def transform(self, data, loggs):
        data = [m for m in data
                if m.pt_range[0] >= self.mrange[0] and
                m.pt_range[1] <= self.mrange[1]]
        signals = [m.mass for m in data]
        for s, m in zip(signals, data):
            if s is None:
                continue
            s.label = m.pt_label
        return signals


class SignalExtractor(TransformerBase):
    def transform(self, data, loggs):
        for s in data:
            if s is None:
                continue
            s.SetAxisRange(0.08, 0.2, "X")
            s.GetListOfFunctions().Clear()
        return data


class SignalScaler(TransformerBase):
    def __init__(self, scale=1):
        self.scale = scale

    def transform(self, data, loggs):
        for h in data:
            if h is None:
                continue
            print(h.GetName(), h.GetBinWidth(0), h.GetNbinsX())
            h.Scale(self.scale)
        return data


class SimpleAnalysis(TransformerBase):

    def __init__(self, options, plot=False):
        super(SimpleAnalysis, self).__init__(plot)
        self.options = options
        self.pipeline = Pipeline([
            ("slice", DataSlicer(options.pt)),
            ("parametrize", InvariantMassExtractor(options.invmass)),
            ("fitmasses", MassFitter(options.invmass)),
            ("cut", SignalCutOff(options.output.ptrange)),
            ("signals", SignalExtractor()),
            ("scale", SignalScaler())
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


class ReadInvariantMassDistribution(TransformerBase):
    def __init__(self, pattern, plot=False):
        super(ReadInvariantMassDistribution, self).__init__(plot)
        self.pattern = pattern

    def transform(self, filename, loggs):
        infile = ROOT.TFile(filename)
        histograms = [k.ReadObj() for k in infile.GetListOfKeys()
                      if self.pattern in k.GetName()]
        histograms = sorted(histograms, key=lambda x: x.GetName())
        names = [h.GetName() for h in histograms]
        print(names)
        return histograms


class DebugMasses(TransformerBase):
    def __init__(self, pattern, plot=False):
        super(DebugMasses, self).__init__(plot)
        self.pipeline = Pipeline([
            ("read", ReadInvariantMassDistribution(pattern, plot)),
            ("decorate", SignalExtractor()),
            ("scale", SignalScaler(0.5))
        ])


def debug_input(prod="low"):
    return DataVault().input(
        "debug efficiency",
        prod,
        n_events=1,
        inputs=('hSparseMgg_proj_0_1_3_yx', ''),
        label=prod)


def move_histogram(source, dest):
    if source is None:
        return

    for i in br.range(dest):
        si = source.FindBin(dest.GetBinCenter(i))
        dest.SetBinContent(i, source.GetBinContent(si))
        dest.SetBinError(i, source.GetBinError(si))


@pytest.fixture
def spmc():
    production = "single #pi^{0}"
    return (
        DataVault().input(production, "low", "PhysEff"),
        DataVault().input(production, "high", "PhysEff"),
    )


@pytest.mark.skip('')
@pytest.mark.onlylocal
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta"
])
def test_masses_efficiency(spmc, particle):
    particle = "#pi^{0}"
    options = CompositeEfficiencyOptions(
        particle,
        ptrange="config/pt-debug.json"
    )
    with open_loggs("mass_test_{}".format(particle)) as loggs:
        MassComparator(options, plot=True).transform(spmc, loggs)


@pytest.fixture
def theory_data():
    return DataVault().file("debug efficiency", "high")


@pytest.fixture
def data():
    return DataVault().input("single #pi^{0}", "high", "PhysEff")


@pytest.mark.onlylocal
@pytest.mark.interactive
def test_different_masses_efficiency(data, theory_data):
    with open_loggs() as loggs:
        theory = DebugMasses("Same").transform(theory_data, loggs)

    templates = [h.Clone() for h in theory]
    for h in templates:
        h.label = "calculated"

    with open_loggs() as loggs:
        estimator = SimpleAnalysis(
            OptionsSPMC(
                particle="#pi^{0}",
                ptrange="config/pt-debug.json"
            )
        )
        experiment = estimator.transform(data, loggs)

    for e, t in zip(experiment, templates):
        move_histogram(e, t)

    Comparator().compare(theory, templates)
