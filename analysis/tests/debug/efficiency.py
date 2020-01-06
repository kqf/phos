from __future__ import print_function
import pytest
import ROOT

from spectrum.vault import DataVault
from spectrum.vault import FVault
from spectrum.options import CompositeEfficiencyOptions, Options
from spectrum.efficiency import Efficiency
from spectrum.comparator import Comparator
from spectrum.pipeline import TransformerBase
from spectrum.pipeline import Pipeline, ReducePipeline
from spectrum.pipeline import ParallelPipeline, FunctionTransformer
from spectrum.pipeline import SingleHistReader
import spectrum.broot as br
from array import array


class StanadrtizeOutput(TransformerBase):
    def __init__(self):
        super(StanadrtizeOutput, self).__init__()
        self.ptedges = Options(pt="config/pt-debug.json").pt.ptedges

    def transform(self, histogram, loggs):
        ohist = ROOT.TH1F(
            histogram.GetName(),
            histogram.GetTitle(),
            len(self.ptedges) - 1,
            array("d", self.ptedges)
        )
        for (content, error, center) in zip(*br.bins(histogram)):
            ibin = ohist.FindBin(center)
            ohist.SetBinContent(ibin, content)
            ohist.SetBinError(ibin, error)
        ohist.Sumw2()
        return ohist


class ReadCompositeDistribution(TransformerBase):
    def __init__(self, options, plot=False, name="h1efficiency"):
        super(ReadCompositeDistribution, self).__init__()
        self.pipeline = ReducePipeline(
            ParallelPipeline([
                ("efficiency-{0}".format(ranges),
                 Pipeline([
                     ("raw_efficiency", SingleHistReader(nevents=1)),
                     ("standard-output", StanadrtizeOutput())
                 ]))
                for ranges in zip(options.mergeranges)
            ]),
            lambda x, loggs: br.sum_trimm(x, options.mergeranges)
        )


class CompareEfficiencies(TransformerBase):
    def __init__(self, options, plot=False):
        super(CompareEfficiencies, self).__init__(plot)
        self.pipeline = ReducePipeline(
            ParallelPipeline([
                ("calculated_efficiency", Efficiency(options)),
                ("read_debug_efficiency", ReadCompositeDistribution(options))
            ]),
            Comparator().compare
        )


class CompareGeneratedSpectra(TransformerBase):
    def __init__(self, options, plot=False):
        super(CompareGeneratedSpectra, self).__init__(plot)
        self.pipeline = ReducePipeline(
            ParallelPipeline([
                ("custom_spectrum", SingleHistReader(nevents=1)),
                ("debug_spectrum", Pipeline([
                    ("single", SingleHistReader(nevents=1)),
                    ("scale", FunctionTransformer(br.scalew))
                ])
                )
            ]),
            Comparator().compare
        )


def debug_input(prod="low"):
    return DataVault().input(
        "debug efficiency",
        prod,
        n_events=1,
        histnames=("hSparseMgg_proj_0_1_3_yx",),
        histname="hGenPi0Pt_clone"
    )


def debug_efficiency_input(prod="low"):
    return DataVault().input(
        "debug efficiency",
        prod,
        n_events=1,
        histnames=("hSparseMgg_proj_0_1_3_yx",),
        histname="h1efficiency",
    )


@pytest.fixture
def debug_inputs():
    return (
        debug_input("low"),
        debug_input("high"),
    )


def debug_options(particle):
    return CompositeEfficiencyOptions(
        particle,
        genname="hGenPi0Pt_clone",
        use_particle=False,
        pt="config/pt-debug.json",
        scale=0.5
    )


def spmc_options(particle):
    options = CompositeEfficiencyOptions(
        particle,
        genname="hPt_{0}_primary_",
        pt="config/pt-debug.json"
    )
    return options


@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    # "#eta"
])
@pytest.mark.parametrize("options", [
    debug_options,
    spmc_options,
])
def test_efficiency_evaluation(particle, debug_inputs, options):
    CompareEfficiencies(options=options(particle=particle)).transform(
        [debug_inputs, debug_inputs],
        "compare the debug efficiency"
    )


@pytest.fixture
def data():
    histname = "hPt_#pi^{0}_primary_standard"
    return (
        DataVault().input("single #pi^{0}", "low", histname=histname),
        DataVault().input("single #pi^{0}", "high", histname=histname),
    )


@pytest.mark.skip("")
@pytest.mark.onlylocal
@pytest.mark.interactive
def test_generated_spectrum(particle, debug_inputs, data):
    CompareGeneratedSpectra(
        CompositeEfficiencyOptions(particle)).transform(
        [data[0], debug_inputs[0]],
        "compare the debug efficiency"
    )


@pytest.fixture
def data_debug_low_single():
    return DataVault().input(
        "debug efficiency", "low", histname="hGenPi0Pt_clone")


@pytest.mark.skip("")
@pytest.mark.onlylocal
@pytest.mark.interactive
def test_weight_like_debug(data_debug_low_single):
    # Define the transformations
    nominal_low = SingleHistReader(nevents=1).transform(data_debug_low_single)

    rrange = 0, 10
    tsallis = ROOT.TF1("f", FVault().func("tsallis"), *rrange)
    tsallis.SetParameters(0.014960701090585591,
                          0.287830380417601, 9.921003040859755)
    tsallis.FixParameter(3, 0.135)
    tsallis.FixParameter(4, 0.135)
    tsallis.SetLineColor(46)

    br.scalew(nominal_low, 1. / nominal_low.Integral())
    nominal_low.Fit(tsallis)
    print(br.pars(tsallis))

    Comparator().compare(nominal_low)
