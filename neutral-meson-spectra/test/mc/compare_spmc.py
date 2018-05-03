import unittest
from spectrum.pipeline import ComparePipeline
from spectrum.efficiency import Efficiency
from spectrum.options import CompositeEfficiencyOptions, EfficiencyOptions

from vault.datavault import DataVault


def define_datasets():
    datasets = [
        {
            DataVault().input("single #pi^{0} iteration3 yield aliphysics", "low"): (0, 7.0),
            DataVault().input("single #pi^{0} iteration3 yield aliphysics", "high"): (7.0, 20)
        },
        DataVault().input("pythia8", "stable"),
        DataVault().input("pythia8", "stable"),
    ]
    names = "aliphysics", "pythia8", "pythia8"
    return names, datasets


class CompareDifferentEfficiencies(unittest.TestCase):

    def test_efficiencies(self):
        names, datasets = define_datasets()
        particle = "#pi^{0}"
        estimator = ComparePipeline([
            (names[0],
                Efficiency(
                    CompositeEfficiencyOptions.spmc(
                        datasets[0],
                        particle,
                        ptrange='config/pt-same.json'
                    )
            ))] + [(name,
                    Efficiency(
                        EfficiencyOptions(
                            genname='hPt_#pi^{0}_primary_',
                            scale=1.8,
                            ptrange='config/pt-same-truncated.json'
                        )
                    )
                    )
                   for name in names[1:]
                   ],
            plot=False
        )

        estimator.transform(
            datasets,
            "compare different datasts"
        )
