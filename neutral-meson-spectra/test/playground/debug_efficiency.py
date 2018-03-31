import unittest

from vault.datavault import DataVault
from spectrum.analysis import Analysis
from spectrum.output import AnalysisOutput
from spectrum.options import Options


class DebugTheEfficiency(unittest.TestCase):

	def test_spectrum_extraction(self):
		estimator = Analysis(Options.spmc((7, 20)))
		loggs = AnalysisOutput("debug_efficiency", "#pi^{0}")
		output = estimator.transform(
			DataVault().input("debug efficiency", "high", nevents=1e6, histnames=('hSparseMgg_proj_0_1_3_yx', '')),
			loggs
		)
		loggs.plot()

