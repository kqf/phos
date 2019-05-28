import pytest
import ROOT

from vault.datavault import DataVault
from vault.formulas import FVault
from spectrum.options import CompositeEfficiencyOptions, Options
from spectrum.efficiency import Efficiency
from spectrum.comparator import Comparator
from spectrum.pipeline import TransformerBase
from spectrum.pipeline import Pipeline, ReducePipeline
from spectrum.pipeline import ParallelPipeline, FunctionTransformer
from spectrum.input import SingleHistInput

from spectrum.broot import BROOT as br
from array import array


class StanadrtizeOutput(TransformerBase):
    def __init__(self):
        super(StanadrtizeOutput, self).__init__()
        self.ptedges = Options(ptrange="config/pt-debug.json").pt.ptedges

    def transform(self, histogram, loggs):
        ohist = ROOT.TH1F(
            histogram.GetName() + histogram.label,
            histogram.GetTitle(),
            len(self.ptedges) - 1,
            array("d", self.ptedges)
        )
        for (content, error, center) in zip(*br.bins(histogram)):
            ibin = ohist.FindBin(center)
            ohist.SetBinContent(ibin, content)
            ohist.SetBinError(ibin, error)
        ohist.Sumw2()
        ohist.label = histogram.label
        return ohist


class ReadCompositeDistribution(TransformerBase):
    def __init__(self, options, plot=False, name="h1efficiency"):
        super(ReadCompositeDistribution, self).__init__()
        self.pipeline = ReducePipeline(
            ParallelPipeline([
                ("efficiency-{0}".format(ranges),
                 Pipeline([
                            ("raw_efficiency", SingleHistInput(name)),
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
    def __init__(self, options, names, plot=False):
        super(CompareGeneratedSpectra, self).__init__(plot)
        self.pipeline = ReducePipeline(
            ParallelPipeline([
                ("custom_spectrum", SingleHistInput(names[0])),
                ("debug_spectrum", Pipeline([
                    ("single", SingleHistInput(names[1])),
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
        inputs=("hSparseMgg_proj_0_1_3_yx", ""),
        label=prod)


@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta"
])
def test_efficiency_evaluation(particle):
    debug_inputs = (
        debug_input("low"),
        debug_input("high"),
    )

    moptions = CompositeEfficiencyOptions(
        particle,
        genname="hGenPi0Pt_clone",
        use_particle=False,
        ptrange="config/pt-debug.json",
        scale=0.5
    )
    # moptions.mergeranges = [(0, 6), (6, 20)]

    # prod = "single #pi^{0}"
    # ll = "debug-ledger.json"
    # inputs = (
    #     DataVault(ll).input(prod, "low", listname="PhysEff"),
    #     DataVault(ll).input(prod, "high", listname="PhysEff"),
    # )

    # moptions = CompositeEfficiencyOptions(
    #     particle,
    #     genname="hPt_{0}_primary_",
    #     ptrange="config/pt-debug.json"
    # )

    # moptions.mergeranges = [(0, 6), (6, 20)]
    CompareEfficiencies(moptions).transform(
        [debug_inputs, debug_inputs],
        "compare the debug efficiency"
    )


@pytest.mark.skip("")
@pytest.mark.onlylocal
@pytest.mark.interactive
def test_generated_spectrum(particle):
    debug_inputs = (
        debug_input("low"),
        debug_input("high"),
    )

    prod = "single #pi^{0}"
    inputs = (
        DataVault().input(prod, "low"),
        DataVault().input(prod, "high"),
    )

    moptions = CompositeEfficiencyOptions(particle)

    names = "hPt_#pi^{0}_primary_standard", "hGenPi0Pt_clone"

    CompareGeneratedSpectra(moptions, names=names).transform(
        [inputs.keys()[0], debug_inputs.keys()[0]],
        "compare the debug efficiency"
    )


@pytest.mark.skip("")
@pytest.mark.onlylocal
@pytest.mark.interactive
def test_weight_like_debug():
    input_low = DataVault().input(
        "debug efficiency", "low", n_events=1e6,
        histnames=("hSparseMgg_proj_0_1_3_yx", ""))

    # Define the transformations
    nominal_low = SingleHistInput("hGenPi0Pt_clone").transform(input_low)

    rrange = 0, 10
    tsallis = ROOT.TF1("f", FVault().func("tsallis"), *rrange)
    tsallis.SetParameters(0.014960701090585591,
                          0.287830380417601, 9.921003040859755)
    tsallis.FixParameter(3, 0.135)
    tsallis.FixParameter(4, 0.135)
    tsallis.SetLineColor(46)

    br.scalew(nominal_low, 1. / nominal_low.Integral())
    nominal_low.Fit(tsallis)
    print br.pars(tsallis)
    Comparator().compare(nominal_low)
