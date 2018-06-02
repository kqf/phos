import unittest
from spectrum.pipeline import ComparePipeline
from spectrum.efficiency import Efficiency
from spectrum.options import CompositeEfficiencyOptions, EfficiencyOptions
from spectrum.options import CompositeOptions
from spectrum.analysis import Analysis
from spectrum.output import AnalysisOutput

from vault.datavault import DataVault


def define_general_datasets():
    datasets = [DataVault().input('pythia8',
                                  'staging',
                                  listname="PhysEff",
                                  histname="MassPt")]
    names = ["pythia8"]
    return names, datasets


def define_composite_datasets():
    datasets = [
        {
            DataVault().input("single #pi^{0} iteration d3 nonlin12",
                              "low",
                              listname="PhysEff" + i): (0, 7.0),
            DataVault().input("single #pi^{0} iteration d3 nonlin12",
                              "high",
                              listname="PhysEff" + i): (7.0, 20)
        }
        for i in ["2"]
    ]

    reference = [
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
    datasets = datasets + reference
    names = "nonlin", "standard", "0.5 standard", "2 standard", "ref"
    return names, datasets


class CompareDifferentEfficiencies(unittest.TestCase):

    def test_efficiencies(self):
        gnames, gdatasets = define_general_datasets()
        names, datasets = define_composite_datasets()
        particle = "#pi^{0}"

        estimators = [
            (name, Efficiency(CompositeEfficiencyOptions(uinput, particle)))
            for name, uinput in zip(names, datasets)
        ]
        estimators += [
            (name, Efficiency(EfficiencyOptions(scale=1.0))) for name in gnames
        ]

        estimator = ComparePipeline(estimators, plot=True)
        estimator.transform(
            datasets + gdatasets,
            loggs=AnalysisOutput("compare different datasts")
        )
