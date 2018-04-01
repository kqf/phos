import unittest

from vault.datavault import DataVault
from spectrum.analysis import Analysis
from spectrum.output import AnalysisOutput
from spectrum.options import EfficiencyOptions
from spectrum.efficiency import Efficiency
from spectrum.comparator import Comparator
from spectrum.transformer import TransformerBase
from spectrum.pipeline import Pipeline
from spectrum.input import SingleHistInput


class DebugTheEfficiency(unittest.TestCase):

	def test_spectrum_extraction(self):
		estimator = Efficiency(
			EfficiencyOptions.spmc(
				(7, 20),
				genname='hGenPi0Pt_clone',
				ptrange='config/pt-debug.json'
			)
		)

		loggs = AnalysisOutput("debug_efficiency", "#pi^{0}")
		inputs = DataVault().input("debug efficiency", "high", n_events=1e6, histnames=('hSparseMgg_proj_0_1_3_yx', ''))

		# Define the transformations
		output = estimator.transform(inputs, loggs)

		nominal = SingleHistInput("h1efficiency").transform(inputs, loggs)
		nominal.label = 'nominal efficiency'

		diff = Comparator(stop=True)
		diff.compare(output, nominal)

		loggs.plot()

