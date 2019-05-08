import pytest
from spectrum.pipeline import ComparePipeline
from spectrum.efficiency import Efficiency
from spectrum.options import EfficiencyOptions
from spectrum.options import CompositeEfficiencyOptions
from vault.datavault import DataVault


def define_datasets():
    production = "single #pi^{0}"
    datasets = (
        (
            DataVault().input(production, "low", "PhysEff"),
            DataVault().input(production, "high", "PhysEff"),
        ),
        DataVault().input("pythia8"),
    )
    names = "spmc", "pythia8"
    return names, datasets


@pytest.mark.onlylocal
def test_efficiencies():
    names, datasets = define_datasets()
    particle = "#pi^{0}"
    composite_options = CompositeEfficiencyOptions(particle)
    options = [(names[0], Efficiency(composite_options))]

    general_options = EfficiencyOptions(
        genname="hPt_#pi^{0}_primary_",
        scale=1.8,
        ptrange="config/pt-same-truncated.json"
    )

    options += [
        (name, Efficiency(general_options)) for name in names[1:]
    ]

    estimator = ComparePipeline(options, plot=False)
    estimator.transform(datasets, {})
