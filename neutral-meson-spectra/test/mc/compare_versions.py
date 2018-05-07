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
            DataVault().input("single #pi^{0} iteration3 yield aliphysics", "low"): (0, 7.0),
            DataVault().input("single #pi^{0} iteration3 yield aliphysics", "high"): (7.0, 20)
        },
        {
            DataVault().input("single #pi^{0} iteration d1", "low"): (0, 7.0),
            DataVault().input("single #pi^{0} iteration d1", "high"): (7.0, 20)
        },
        {
            DataVault().input("single #pi^{0} iteration d2", "low"): (0, 7.0),
            DataVault().input("single #pi^{0} iteration d2", "high"): (7.0, 20)
        },
    ]
    names = "w0", "w1", "w2"
    return names, datasets


class CompareDifferentEfficiencies(unittest.TestCase):

    @unittest.skip('')
    def test_efficiencies(self):
        names, datasets = define_datasets()
        particle = "#pi^{0}"
        estimator = ComparePipeline([
            (name,
                Efficiency(CompositeEfficiencyOptions.spmc(uinput, particle)))
            for name, uinput in zip(names, datasets)
        ])

        estimator.transform(
            datasets,
            "compare different datasts"
        )


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
