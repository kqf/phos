import unittest

from spectrum.options import Options
from spectrum.analysis import Analysis
from spectrum.comparator import Comparator
from spectrum.broot import BROOT as br
from spectrum.transformer import TransformerBase
from spectrum.pipeline import ParallelPipeline, ReducePipeline
from spectrum.output import AnalysisOutput

from vault.datavault import DataVault


class CompareAnalysis(TransformerBase):
    def __init__(self, steps, particle):
        super(CompareAnalysis, self).__init__()
        options = Options(particle=particle)
        options.output.scalew_spectrum = True
        self.pipeline = ReducePipeline(
            ParallelPipeline([(step, Analysis(options)) for step in steps]),
            Comparator(labels=steps).compare
        )

def compare_for_particle(particle):
    data = (
        DataVault().input("data", "LHC17 qa1", label="2017"),
        DataVault().input("data", label="2016"),
    )


    estimator = CompareAnalysis(
        steps=[d.label for d in data],
        particle=particle
    )

    loggs = AnalysisOutput("compare different datasets", particle=particle)
    estimator.transform(data, loggs)
    loggs.plot()


class TestCompareDatasets(unittest.TestCase):

    def test_gives_similar_results_for_pions(self):
        compare_for_particle("#pi^{0}")

    def test_gives_similar_results_for_eta(self):
        compare_for_particle("#eta")
