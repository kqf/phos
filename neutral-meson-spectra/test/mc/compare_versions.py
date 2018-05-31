import unittest
from spectrum.pipeline import ComparePipeline
from spectrum.efficiency import Efficiency
from spectrum.options import CompositeEfficiencyOptions, Options
from spectrum.options import CompositeOptions
from spectrum.analysis import Analysis
from spectrum.output import AnalysisOutput

from vault.datavault import DataVault


def define_datasets():
    datasets = [
        {
            DataVault().input("single #pi^{0} iteration d3 nonlin11",
                              "low",
                              listname="PhysEff" + i): (0, 7.0),
            DataVault().input("single #pi^{0} iteration d3 nonlin11",
                              "high",
                              listname="PhysEff" + i): (7.0, 20)
        }
        for i in ["", "1", "2", "3"]
    ]
    # datasets = datasets + [
    #     {
    #         DataVault().input("single #pi^{0} iteration d3 nonlin4",
    #                           "low",
    #                           listname="PhysEff" + i): (0, 7.0),
    #         DataVault().input("single #pi^{0} iteration d3 nonlin4",
    #                           "high",
    #                           listname="PhysEff" + i): (7.0, 20)
    #     }
    #     for i in ["1", "2", "3"]
    # ]
    datasets = datasets + [
        # {
        #     DataVault().input("single #pi^{0} iteration3 yield",
        #                       "low"): (0, 7.0),
        #     DataVault().input("single #pi^{0} iteration3 yield",
        #                       "high"): (7.0, 20)
        # },
        {
            DataVault().input("single #pi^{0} iteration3 yield aliphysics",
                              "low",
                              listname="PhysEff",
                              ): (0, 7.0),
            DataVault().input("single #pi^{0} iteration3 yield aliphysics",
                              "high",
                              listname="PhysEff",
                              ): (7.0, 20)
        },
    ]
    names = "p1", "p2", "p3", "n1", "n2", "n3", "initial param"
    return names, datasets


class CompareDifferentEfficiencies(unittest.TestCase):

    def test_efficiencies(self):
        names, datasets = define_datasets()
        particle = "#pi^{0}"
        estimator = ComparePipeline([
            (name,
                Efficiency(
                    CompositeEfficiencyOptions.spmc(uinput,
                                                    particle,
                                                    # ptrange='config/pt-dummy.json'
                                                    )))
            for name, uinput in zip(names, datasets)
        ], plot=True)

        estimator.transform(
            datasets,
            loggs=AnalysisOutput("compare different datasts")
        )


@unittest.skip('')
class CompareRawYields(unittest.TestCase):

    def test_yields(self):
        names, datasets = define_datasets()
        particle = "#pi^{0}"
        data = [('data', Analysis(Options()))]
        estimator = ComparePipeline(data + [
            (name,
                Analysis(CompositeOptions.spmc(uinput, particle)))
            for name, uinput in zip(names, datasets)
        ], True)

        estimator.transform(
            [DataVault().input("data")] + datasets,
            "compare different datasts"
        )
