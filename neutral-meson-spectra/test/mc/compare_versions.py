import unittest
from spectrum.pipeline import ComparePipeline
from spectrum.efficiency import Efficiency
from spectrum.options import CompositeEfficiencyOptions, Options
from spectrum.options import CompositeOptions
from spectrum.analysis import Analysis

from vault.datavault import DataVault


def define_datasets():
    datasets = [
        {
            DataVault().input("single #pi^{0} iteration d3 debug",
                              "low",
                              listname="PhysEffPlain" + i): (0, 7.0),
            DataVault().input("single #pi^{0} iteration d3 debug",
                              "high",
                              listname="PhysEffPlain" + i): (7.0, 20)
        }
        for i in ["3"]
    ]
    datasets = datasets + [
        {
            DataVault().input("single #pi^{0} iteration d3 debug1",
                              "low",
                              listname="PhysEffPlain" + i): (0, 7.0),
            DataVault().input("single #pi^{0} iteration d3 debug1",
                              "high",
                              listname="PhysEffPlain" + i): (7.0, 20)
        }
        for i in ["3"]
    ]
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
                              listname="PhysEffPlain",
                              ): (0, 7.0),
            DataVault().input("single #pi^{0} iteration3 yield aliphysics",
                              "high",
                              listname="PhysEffPlain",
                              ): (7.0, 20)
        },
    ]
    names = "debug1", "debug2", "initial param"
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
        ])

        estimator.transform(
            datasets,
            "compare different datasts"
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
        ])

        estimator.transform(
            [DataVault().input("data")] + datasets,
            "compare different datasts"
        )
