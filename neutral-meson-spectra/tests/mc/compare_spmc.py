import unittest
from spectrum.pipeline import ComparePipeline
from spectrum.efficiency import Efficiency
from spectrum.options import CompositeEfficiencyOptions, EfficiencyOptions

from vault.datavault import DataVault


def define_datasets():
    production = "single #pi^{0}"
    datasets = (
        {
            DataVault().input(production, "low"): (0, 7.0),
            DataVault().input(production, "high"): (7.0, 20)
        },
        DataVault().input("pythia8", "stable"),
        DataVault().input("pythia8", "stable"),
    )
    names = "aliphysics", "pythia8", "pythia8"
    return names, datasets


class CompareDifferentEfficiencies(unittest.TestCase):

    def test_efficiencies(self):
        names, datasets = define_datasets()
        particle = "#pi^{0}"
        composite_options = CompositeEfficiencyOptions(datasets[0], particle)
        options = [(names[0], Efficiency(composite_options))]

        general_options = EfficiencyOptions(
            genname='hPt_#pi^{0}_primary_',
            scale=1.8,
            ptrange='config/pt-same-truncated.json'
        )

        options += [
            (name, Efficiency(general_options)) for name in names[1:]
        ]

        estimator = ComparePipeline(options, plot=False)
        estimator.transform(datasets, "compare different datasts")
