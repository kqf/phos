import unittest
import ROOT

from vault.datavault import DataVault
from spectrum.options import CompositeEfficiencyOptions, Options
from spectrum.efficiency import Efficiency
from spectrum.comparator import Comparator
from spectrum.transformer import TransformerBase
from spectrum.pipeline import Pipeline, ReducePipeline,
from spectrum.pipeline import ParallelPipeline, FunctionTransformer
from spectrum.input import SingleHistInput

from spectrum.broot import BROOT as br
from array import array


class StanadrtizeOutput(TransformerBase):
    def __init__(self):
        super(StanadrtizeOutput, self).__init__()
        self.ptedges = Options(ptrange="config/pt-debug-full.json").pt.ptedges

    def transform(self, histogram, loggs):
        ohist = ROOT.TH1F(
            histogram.GetName() + histogram.label,
            histogram.GetTitle(),
            len(self.ptedges) - 1,
            array('d', self.ptedges)
        )
        for (content, error, center) in zip(*br.bins(histogram)):
            ibin = ohist.FindBin(center)
            ohist.SetBinContent(ibin, content)
            ohist.SetBinError(ibin, error)
        ohist.Sumw2()
        ohist.label = histogram.label
        return ohist


class ReadCompositeDistribution(TransformerBase):
    def __init__(self, options, plot=False, name='h1efficiency'):
        super(ReadCompositeDistribution, self).__init__()
        self.pipeline = ReducePipeline(
            ParallelPipeline([
                ("efficiency-{0}".format(ranges),
                 Pipeline([
                            ("raw_efficiency", SingleHistInput(name)),
                            ("standard-output", StanadrtizeOutput())
                 ])
                 )
                for ranges in zip(options.mergeranges)
            ]
            ),
            lambda x: br.sum_trimm(x, options.mergeranges)
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
                # ("custom_spectrum", ReadCompositeDistribution(options, name=names[0])),
                # ("debug_spectrum", ReadCompositeDistribution(options, name=names[1]))
                ("custom_spectrum", SingleHistInput(names[0])),
                ("debug_spectrum", Pipeline([
                    ("single", SingleHistInput(names[1])),
                    ("scale", FunctionTransformer(br.scalew))
                ])
                )
            ]),
            Comparator().compare
        )


class DebugTheEfficiency(unittest.TestCase):

    def test_efficiency_evaluation(self):
        particle = "#pi^{0}"
        debug_inputs = {
            DataVault().input("debug efficiency", "low", n_events=1, histnames=('hSparseMgg_proj_0_1_3_yx', ''), label="low"): (0, 6),
            DataVault().input("debug efficiency", "high", n_events=1, histnames=('hSparseMgg_proj_0_1_3_yx', ''), label="high"): (6, 20)
        }

        # moptions = CompositeEfficiencyOptions.spmc(
        #     debug_inputs,
        #     particle,
        #     genname='hGenPi0Pt_clone',
        #     use_particle=False,
        #     ptrange="config/pt-debug-full.json"
        # )

        unified_inputs = {
            DataVault().input("single #pi^{0} corrected weights", "low"): (0, 7.0),
            DataVault().input("single #pi^{0} corrected weights", "high"): (7.0, 20)
        }

        moptions = CompositeEfficiencyOptions.spmc(
            unified_inputs,
            particle,
            genname='hPt_{0}_primary_standard',
            ptrange="config/pt-debug-full.json"
        )

        compared = CompareEfficiencies(moptions).transform(
            [unified_inputs, debug_inputs],
            "compare the debug efficiency"
        )

    @unittest.skip('')
    def test_generated_spectrum(self):
        particle = "#pi^{0}"
        debug_inputs = {
            DataVault().input("debug efficiency", "low", n_events=1, histnames=('hSparseMgg_proj_0_1_3_yx', ''), label="low"): (0, 6),
            DataVault().input("debug efficiency", "high", n_events=1, histnames=('hSparseMgg_proj_0_1_3_yx', ''), label="high"): (6, 20)
        }

        unified_inputs = {
            DataVault().input("single #pi^{0} corrected weights", "low"): (0, 7.0),
            DataVault().input("single #pi^{0} corrected weights", "high"): (7.0, 20)
        }

        moptions = CompositeEfficiencyOptions.spmc(unified_inputs, particle)

        names = 'hPt_#pi^{0}_primary_standard', 'hGenPi0Pt_clone'

        compared = CompareGeneratedSpectra(moptions, names=names).transform(
            [unified_inputs.keys()[0], debug_inputs.keys()[0]],
            "compare the debug efficiency"
        )

    @unittest.skip('')
    def test_weight_like_debug(self):
        input_low = DataVault().input(
            "debug efficiency", "low", n_events=1e6,
            histnames=('hSparseMgg_proj_0_1_3_yx', ''))

        # Define the transformations
        nominal_low = SingleHistInput("hGenPi0Pt_clone").transform(input_low)

        rrange = 0, 10
        tsallis = ROOT.TF1(
            "f", "x[0] * (x[0] )*[0]/2./3.1415*([2]-1.)*([2]-2.)/([2]*[1]*([2]*[1]+[4]*([2]-2.))) * (1.+(sqrt((x[0])*(x[0])+[3]*[3])-[4])/([2]*[1])) ** (-[2])", *rrange)
        tsallis.SetParameters(0.014960701090585591,
                              0.287830380417601, 9.921003040859755)
        tsallis.FixParameter(3, 0.135)
        tsallis.FixParameter(4, 0.135)
        tsallis.SetLineColor(46)

        br.scalew(nominal_low, 1. / nominal_low.Integral())
        nominal_low.Fit(tsallis)
        print br.pars(tsallis)
        Comparator().compare(nominal_low)
