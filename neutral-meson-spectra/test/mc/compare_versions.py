import unittest
from spectrum.pipeline import ComparePipeline
from spectrum.efficiency import Efficiency
from spectrum.options import MultirangeEfficiencyOptions

from vault.datavault import DataVault


def define_datasets():
    datasets = [
        {
            DataVault().input("single #pi^{0} iteration3 yield aliphysics", "low"): (0, 7.0),
            DataVault().input("single #pi^{0} iteration3 yield aliphysics", "high"): (7.0, 20)
        },
        {
            DataVault().input("single #pi^{0} iteration3 yield", "low"): (0, 7.0),
            DataVault().input("single #pi^{0} iteration3 yield", "high"): (7.0, 20)
        },
    ]
    names = "old", "aliphysics"
    return names, datasets


class CompareDifferentEfficiencies(unittest.TestCase):

    def test_efficiencies(self):
        names, datasets = define_datasets()
        particle = "#pi^{0}"
        estimator = ComparePipeline([
            (name, Efficiency(MultirangeEfficiencyOptions.spmc(uinput, particle))) for name, uinput in zip(names, datasets)
        ])

        estimator.transform(
            datasets,
            "compare different datasts"
        )
