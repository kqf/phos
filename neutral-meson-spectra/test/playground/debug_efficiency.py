import unittest

from vault.datavault import DataVault
from spectrum.analysis import Analysis
from spectrum.output import AnalysisOutput
from spectrum.options import EfficiencyOptions, MultirangeEfficiencyOptions
from spectrum.efficiency import Efficiency, EfficiencyMultirange
from spectrum.comparator import Comparator
from spectrum.transformer import TransformerBase
from spectrum.pipeline import Pipeline, ReducePipeline, ParallelPipeline
from spectrum.input import SingleHistInput

class DebugTheEfficiency(unittest.TestCase):

    @unittest.skip("")
    def test_spectrum_extraction(self):
        estimator = Efficiency(
            EfficiencyOptions.spmc(
                (7, 20),
                genname='hGenPi0Pt_clone',
                ptrange='config/pt-debug.json'
            )
        )

        loggs = AnalysisOutput("debug_efficiency", "#pi^{0}")
        input_high = DataVault().input("debug efficiency", "high", n_events=1e6, histnames=('hSparseMgg_proj_0_1_3_yx', ''))

        # Define the transformations
        output = estimator.transform(input_high, loggs)

        nominal_high = SingleHistInput("h1efficiency").transform(input_high, loggs)
        nominal_high.label = 'nominal efficiency'

        diff = Comparator(stop=True)
        diff.compare(output, nominal_high)

        loggs.plot()

        input_low = DataVault().input("debug efficiency", "low", n_events=1e6, histnames=('hSparseMgg_proj_0_1_3_yx', ''))
        nominal_low = SingleHistInput("h1efficiency").transform(input_low, loggs)
        nominal_low.label = 'low p_{T}'
        nominal_high.label = 'high p_{T}'
        diff.compare(nominal_low, nominal_high)

    def test_calculates_full_efficiency(self):
        particle = "#pi^{0}"
        unified_inputs = {
            DataVault().input("debug efficiency", "low", n_events=1e6, histnames=('hSparseMgg_proj_0_1_3_yx', '')): (0, 7),
            DataVault().input("debug efficiency", "high", n_events=1e6, histnames=('hSparseMgg_proj_0_1_3_yx', '')): (7, 20)
        }
        moptions = MultirangeEfficiencyOptions.spmc(unified_inputs, particle)
        for options in moptions.suboptions:
            options.genname = "hGenPi0Pt_clone"

            # options.analysis.signalp.relaxed = True
            # options.analysis.backgroundp.relaxed = True

        estimator = EfficiencyMultirange(moptions)

        loggs = AnalysisOutput("debug_composite_efficiency_spmc_{}".format(particle), particle)
        efficiency = estimator.transform(unified_inputs.keys(), loggs)

        efficiency.SetTitle(
            "#varepsilon = #Delta #phi #Delta y/ 2 #pi " \
            "#frac{Number of reconstructed %s}{Number of generated primary %s}" \
            % (particle, particle)
        )
        diff = Comparator()
        diff.compare(efficiency)
        loggs.plot(False)

