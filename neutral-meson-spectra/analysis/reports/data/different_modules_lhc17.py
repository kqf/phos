import unittest
import pytest

from spectrum.analysis import Analysis
from spectrum.options import Options
from spectrum.output import AnalysisOutput
from spectrum.pipeline import ComparePipeline
from vault.datavault import DataVault


def analyze(inputs, particle="#pi^{0}"):
    options = Options(
        particle=particle,
        ptrange="config/test_different_modules.json"
    )
    estimator = ComparePipeline([
        ('module {0}'.format(i), Analysis(options))
        for i, _ in enumerate(inputs)
    ])

    loggs = AnalysisOutput("compare_different_modules", particle=particle)
    estimator.transform(inputs, loggs)
    loggs.plot()


class TestCheckModules(unittest.TestCase):
    @pytest.mark.onlylocal
    def test_different_modules_pi0(self):
        inputs = DataVault().modules_input("data", "LHC17 qa1", "Phys", True)
        analyze(inputs, "#pi^{0}")

    @pytest.mark.onlylocal
    def test_different_modules_eta(self):
        inputs = DataVault().modules_input("data", "LHC17 qa1", "Phys", True)
        analyze(inputs, "#eta")
